#!/usr/bin/env python3
"""Exercise native app-server manual compaction with continuation canaries."""

from __future__ import annotations

import argparse
import json
import select
import subprocess
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "NATIVE-GOAL-410",
    "NATIVE-ACCEPT-411",
    "src/native/compactor.rs",
    "cargo test -p native-compactor",
    "NATIVE-AUTH-412",
    "NATIVE-NEXT-413",
]
FORBIDDEN = ["NATIVE-RAW-DROP-419"]
TRANSCRIPT = """We are continuing objective NATIVE-GOAL-410. Acceptance marker NATIVE-ACCEPT-411 requires preserving the public API and running `cargo test -p native-compactor`. The relevant file is `src/native/compactor.rs`. Authorization boundary NATIVE-AUTH-412 says no dependency installation or external write. The next action NATIVE-NEXT-413 is inspect the existing implementation, then run the named test. The implementation is still unverified. Repeated raw runner noise follows and has already been summarized: NATIVE-RAW-DROP-419 frame=1 frame=2 frame=3. Do not call tools. Reply exactly READY."""
FOLLOW_UP = """Do not call tools. From the compacted conversation, return a concise continuation handoff containing the exact active goal marker, acceptance marker, relevant file path, validation command, authorization-boundary marker, and next-action marker. Omit disposable raw-log noise."""


class Client:
    def __init__(self) -> None:
        self.process = subprocess.Popen(
            ["codex", "app-server", "--strict-config", "--disable", "remote_compaction_v2", "--stdio"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            cwd=ROOT,
        )
        self.events: list[dict[str, Any]] = []
        self.next_id = 1
        self.notification_cursor = 0

    def send(self, method: str, params: dict[str, Any] | None = None) -> int:
        request_id = self.next_id
        self.next_id += 1
        payload = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            payload["params"] = params
        assert self.process.stdin is not None
        self.process.stdin.write(json.dumps(payload) + chr(10))
        self.process.stdin.flush()
        return request_id

    def notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        payload = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params
        assert self.process.stdin is not None
        self.process.stdin.write(json.dumps(payload) + chr(10))
        self.process.stdin.flush()

    def read(self, timeout: float = 120.0) -> dict[str, Any]:
        assert self.process.stdout is not None
        ready, _, _ = select.select([self.process.stdout], [], [], timeout)
        if not ready:
            raise TimeoutError("timed out waiting for app-server")
        line = self.process.stdout.readline()
        if not line:
            stderr = self.process.stderr.read() if self.process.stderr else ""
            raise RuntimeError(f"app-server exited early: {stderr[-1000:]}")
        event = json.loads(line)
        self.events.append(event)
        return event

    def response(self, request_id: int, timeout: float = 120.0) -> dict[str, Any]:
        deadline = time.monotonic() + timeout
        while True:
            event = self.read(max(0.1, deadline - time.monotonic()))
            if event.get("id") == request_id:
                if "error" in event:
                    raise RuntimeError(f"RPC error: {event["error"]}")
                return event["result"]

    def notification(self, method: str, timeout: float = 180.0) -> dict[str, Any]:
        deadline = time.monotonic() + timeout
        while True:
            for index in range(self.notification_cursor, len(self.events)):
                event = self.events[index]
                if event.get("method") == method:
                    self.notification_cursor = index + 1
                    return event.get("params") or {}
            self.read(max(0.1, deadline - time.monotonic()))

    def wait_idle(self, thread_id: str, start_index: int, timeout: float = 180.0) -> None:
        deadline = time.monotonic() + timeout
        index = start_index
        while True:
            while index < len(self.events):
                event = self.events[index]
                index += 1
                if event.get("method") == "thread/status/changed":
                    params = event.get("params") or {}
                    if params.get("threadId") == thread_id and (params.get("status") or {}).get("type") == "idle":
                        return
            self.read(max(0.1, deadline - time.monotonic()))

    def wait_compaction_terminal(self, thread_id: str, start_index: int, timeout: float = 300.0) -> str:
        deadline = time.monotonic() + timeout
        index = start_index
        compacted = False
        terminal_status = ""
        while True:
            while index < len(self.events):
                event = self.events[index]
                index += 1
                method = event.get("method")
                params = event.get("params") or {}
                item = params.get("item") or {}
                if method == "item/completed" and item.get("type") == "contextCompaction":
                    compacted = True
                elif method == "thread/status/changed" and params.get("threadId") == thread_id:
                    status = (params.get("status") or {}).get("type")
                    if status in {"idle", "systemError"}:
                        terminal_status = status
                if compacted and terminal_status:
                    return terminal_status
            self.read(max(0.1, deadline - time.monotonic()))

    def close(self) -> None:
        if self.process.poll() is None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
                self.process.wait(timeout=5)


def agent_text(turn: dict[str, Any]) -> str:
    texts: list[str] = []
    for item in turn.get("items", []):
        if item.get("type") == "agentMessage":
            text = item.get("text")
            if isinstance(text, str):
                texts.append(text)
    return chr(10).join(texts)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    client = Client()
    try:
        init_id = client.send("initialize", {"clientInfo": {"name": "native-compaction-eval", "version": "1"}, "capabilities": {"experimentalApi": True}})
        client.response(init_id)
        client.notify("initialized")
        start_id = client.send("thread/start", {
            "cwd": str(ROOT), "ephemeral": True, "model": "gpt-5.6-sol",
            "approvalPolicy": "never", "sandbox": "read-only",
            "config": {"model_reasoning_effort": "medium", "experimental_compact_prompt_file": str(ROOT / "prompts/default-compact.md")},
        })
        started = client.response(start_id)
        thread_id = started["thread"]["id"]
        first_index = len(client.events)
        first_id = client.send("turn/start", {"threadId": thread_id, "input": [{"type": "text", "text": TRANSCRIPT}]})
        client.response(first_id)
        client.wait_idle(thread_id, first_index)
        compact_index = len(client.events)
        compact_id = client.send("thread/compact/start", {"threadId": thread_id})
        client.response(compact_id, timeout=240.0)
        wake_id = client.send("thread/read", {"threadId": thread_id, "includeTurns": False})
        client.response(wake_id)
        compact_status = client.wait_compaction_terminal(thread_id, compact_index)
        continuation = ""
        if compact_status == "idle":
            second_index = len(client.events)
            second_id = client.send("turn/start", {"threadId": thread_id, "input": [{"type": "text", "text": FOLLOW_UP}]})
            client.response(second_id)
            client.wait_idle(thread_id, second_index, timeout=240.0)
        for event in reversed(client.events):
            params = event.get("params") or {}
            item = params.get("item") or {}
            if event.get("method") == "item/completed" and item.get("type") == "agentMessage":
                text = item.get("text") or ""
                if text and text != "READY":
                    continuation = text
                    break
        missing = [token for token in REQUIRED if token not in continuation]
        leaked = [token for token in FORBIDDEN if token in continuation]
        compact_items = [(event.get("params") or {}).get("item") for event in client.events if event.get("method") == "item/completed" and ((event.get("params") or {}).get("item") or {}).get("type") == "contextCompaction"]
        output = {
            "thread_id": thread_id, "ephemeral": True, "compact_status": compact_status,
            "compact_prompt_sha256": __import__("hashlib").sha256((ROOT / "prompts/default-compact.md").read_bytes()).hexdigest(),
            "required": REQUIRED, "forbidden": FORBIDDEN,
            "missing": missing, "leaked": leaked,
            "context_compaction_items": len(compact_items),
            "continuation": continuation,
            "passed": not missing and not leaked and bool(compact_items),
            "events": client.events,
        }
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(output, indent=2) + chr(10))
        print("PASS" if output["passed"] else "FAIL")
        print(f"missing={missing} leaked={leaked} compaction_items={len(compact_items)}")
        raise SystemExit(0 if output["passed"] else 1)
    finally:
        if not args.output.exists():
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps({"passed": False, "events": client.events}, indent=2) + chr(10))
        client.close()


if __name__ == "__main__":
    main()
