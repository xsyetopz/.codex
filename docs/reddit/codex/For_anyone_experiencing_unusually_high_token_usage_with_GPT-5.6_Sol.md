#For anyone experiencing unusually high token usage with GPT-5.6 Sol [Visit](https://www.reddit.com/r/codex/comments/1utumqd/for_anyone_experiencing_unusually_high_token/)
### **Subreddit:** [r/codex](https://www.reddit.com/r/codex)
### **Author:** [nseavia71501](https://www.reddit.com/user/nseavia71501/)
### **Vote:** 58
---
Under the current MultiAgent V2 behavior, subagents spawned by Sol can inherit the parent model and reasoning effort. That means a parent running `gpt-5.6-sol` at `xhigh` may spawn every child as Sol at `xhigh`, even when a lighter model is configured for the custom agent. That burns through tokens quickly.
By default, V2 also hides the relevant spawn metadata and controls. You cannot see or explicitly set fields such as `agent_type`, `model`, `reasoning_effort`, or `service_tier` through the exposed tool schema, making it much harder to identify what each child agent is actually running.
The underlying issue appears to be that GPT-5.6 selects the V2 multi-agent schema. The exposed `task_name` field only identifies the task path. It does not select the corresponding configured `[agents.<role>]`.
V2 also defaults `fork_turns` to `all`, which initializes each child with the parent’s persisted conversation history unless the spawn call explicitly uses `fork_turns: "none"` or a bounded number of turns.
GPT-5.5 using V1 correctly applies the same custom-agent role configuration.
There is already an open GitHub issue: [https://github.com/openai/codex/issues/31814](https://github.com/openai/codex/issues/31814)
Until OpenAI releases a proper fix, there are two available workarounds.
**Option 1: Continue using V2 and expose the routing controls**
Add this to `~/.codex/config.toml`:
[features.multi_agent_v2]
hide_spawn_agent_metadata = false
tool_namespace = "agents"Then ensure that each `spawn_agent` call explicitly uses:
fork_turns: "none"Alternatively, use a small bounded turn count when the child genuinely needs recent context.
Note that `fork_turns` is a `spawn_agent` argument. It is not a valid configuration field under `[features.multi_agent_v2]`.
Start a fresh Codex session after changing the configuration. Existing threads may retain the previous tool schema.
References:
[https://github.com/openai/codex/issues/31814#issuecomment-4932285996](https://github.com/openai/codex/issues/31814#issuecomment-4932285996)
[https://github.com/openai/codex/issues/31814#issuecomment-4936638249](https://github.com/openai/codex/issues/31814#issuecomment-4936638249)
**Option 2: Force GPT-5.6 back to the V1 multi-agent schema**
Add this to `~/.codex/config.toml`:
model_catalog_json = "~/.codex/models-v1.json"
[features]
multi_agent = true
multi_agent_v2 = falseThen create `~/.codex/models-v1.json` by copying the current model catalog. In the existing Sol entry, change only:
"slug": "gpt-5.6-sol",
"multi_agent_version": "v1"Optionally, make the same change for Terra:
"slug": "gpt-5.6-terra",
"multi_agent_version": "v1"Do not create a model catalog containing only those fragments. Copy the complete current catalog and edit the matching entries.
Reference:
[https://github.com/openai/codex/issues/31814#issuecomment-4929535353](https://github.com/openai/codex/issues/31814#issuecomment-4929535353)
Applying these workarounds has significantly reduced my token drain. The largest reduction came from restoring control over the child model and reasoning effort while preventing every subagent from receiving the parent’s complete conversation history.
---
## Comments 22

- by [unknown](#) **&#x21C5; 12**
  <br/> Something else to keep in mind, subagents all spawn with fast mode, and I haven't found a way to turn it off. Default isn't exposed. Will report back.

- by [unknown](#) **&#x21C5; 4**
  <br/> ohhhh that would be explanatory

- by [unknown](#) **&#x21C5; 3**
  <br/> Just omitting service tier apparently does it, it inherits parents default.

- by [unknown](#) **&#x21C5; 2**
  <br/> alright ... now this would explain why I blew through my quote on 5x like nothing

- by [unknown](#) **&#x21C5; 10**
  <br/> It’s very apparent that these new models and harness were shipped before being ready.

- by [unknown](#) **&#x21C5; 2**
  <br/> Because they want people to experiment. The labs are trying to determine who sinks or swims.

just a theory.

- by [unknown](#) **&#x21C5; 4**
  <br/> Thanks for this. I found that you can start a new conversation with 5.4 and just be like "hello" and then switch to a 5.6 model. It'll use the old subagent process, and respect custom subagents in `~/.codex/agents/`.

- by [unknown](#) **&#x21C5; 4**
  <br/> Funny you mention that, i just did the same fix on my end.

- by [unknown](#) **&#x21C5; 2**
  <br/> Just popping in here to say option 1 worked for me!

- by [unknown](#) **&#x21C5; 2**
  <br/> Check my recent post. Context above 272k is still billed at 2x usage but the new default window is set to 353k. So 2x is on by default

- by [unknown](#) **&#x21C5; 3**
  <br/> That would only apply to the long context portion not the entire window. And there's no mention that its billed at 2x for sub users.

- by [unknown](#) **&#x21C5; 1**
  <br/> Would you mind sharing how you are capping the context window size?

- by [unknown](#) **&#x21C5; 1**
  <br/> It’s in the config file. You can just ask codex to change it

- by [unknown](#) **&#x21C5; 1**
  <br/> in config.toml you can set auto compaction to 272k to avoide this

- by [unknown](#) **&#x21C5; 1**
  <br/> That was debunked.

- by [unknown](#) **&#x21C5; 1**
  <br/> I think, I found another thing. I am not sure how much tokens are actually used by the auto-review but I had substantial amount of requests.

I enabled it before and forgot about it, and today I was using “Auto Decide Approvals”.

EDIT: It was less than 1$ so not the real issue

[https://learn.chatgpt.com/docs/sandboxing/auto-review](https://learn.chatgpt.com/docs/sandboxing/auto-review)


       [](https://preview.redd.it/for-anyone-experiencing-unusually-high-token-usage-with-gpt-v0-bopjgwwnznch1.png?width=616&format=png&auto=webp&s=e2ca0cb1011be0eb3545a9edf0a1cac0399e8e9e)

- by [unknown](#) **&#x21C5; 1**
  <br/> Is not the default v1 unless you choose to opt in for v2? V2 is the beta testing version right?

- by [unknown](#) **&#x21C5; 1**
  <br/> I sometimes use junie in android studio sometimes, every new chat resets back to sol and they dont expose the speeds so have to assume xhigh all the time. I didn't notice the jump from terra back to sol until I burned through 2 5hr windows with 1 reset in 1 1/2 hours. Got lots done in that time, I had 4 repos open all working through different projects. Luckily I ran out in time to watch the England match...

- by [unknown](#) **&#x21C5; 1**
  <br/> I did this earlier and it helped subagent spawning, but it seemed to break the background agent view in the VSCode extension. If you add this as a hack, you may need to remember to back it out whenever the actual fix lands.

- by [unknown](#) **&#x21C5; 1**
  <br/> Thanks! This is what was causing my usage drain

- by [unknown](#) **&#x21C5; 1**
  <br/> I just switched to Oh My Pi, token consumption and management of subagents and models for them are a little better

- by [unknown](#) **&#x21C5; 1**
  <br/> I am glad I use pi with custom extensions instead :)
