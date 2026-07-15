#GPT-5.6 Sol / Codex Release Discussion Megathread [Visit](https://www.reddit.com/r/codex/comments/1urw0c3/gpt56_sol_codex_release_discussion_megathread/)
### **Subreddit:** [r/codex](https://www.reddit.com/r/codex)
### **Author:** [Drogon2737](https://www.reddit.com/user/Drogon2737/)
### **Vote:** 414
---
The release is expected in the next few minutes, so I figured it would be useful to have a single thread for first impressions, issues, and early testing.
For anyone jumping in right away, post what you notice:
- Codex coding performance
- Debugging quality
- Speed/rate limits
- Larger repo handling
- UI or workflow changes
- Weird bugs or regressions
- Anything that feels noticeably better or worse than the previous version
Once people get access, share your real examples, screenshots, benchmarks, or first impressions here.
**Edit:** OpenAI’s official GPT-5.6 page says it is **“available starting today across ChatGPT, Codex, and the OpenAI API” with the rollout starting globally now and continuing toward full availability over the next 24 hours.** [https://openai.com/index/gpt-5-6/](https://openai.com/index/gpt-5-6/)
The lineup is Sol, Terra, and Luna. Sol is the flagship, Terra is the lower-cost tier, and Luna is the fastest/most affordable tier.
---
## Comments 697

- by [unknown](#) **&#x21C5; 1**
  <br/> Does a reset saying it's expiring on a certain date mean it expires the minute it hits that date local time or PT? Or at some time within that date

- by [unknown](#) **&#x21C5; 2**
  <br/> Codex usage with gpt 5.6 sol has seriously dipped I just bought the 5x plan today and been using Sol with high reasoning effort and one ultra task that went on for like 3hrs (Sol is insanely slow btw) and its already down to 56%, I feel like I wasted my money switching from Claude Code, fable somehow gave me way more usage 🤦‍♂️


       [](https://preview.redd.it/gpt-5-6-sol-codex-release-discussion-megathread-v0-4skyy5ov1och1.png?width=1008&format=png&auto=webp&s=765f6a7b30b4d086c49ee0be780b63abf2f6131c)

- by [unknown](#) **&#x21C5; 1**
  <br/> Dude, wtf. All the models running significantly slower across the board. Giving $100 and $200 sub tiers free GPT-5.6 Sol Ultra credits, there’s no way they can maintain the same traditional inference budget. So gay.

- by [unknown](#) **&#x21C5; 2**
  <br/> Is it just me or 5.6 is extremely slow? I've tried Sol and Luna.

- by [unknown](#) **&#x21C5; 1**
  <br/> [](https://preview.redd.it/gpt-5-6-sol-codex-release-discussion-megathread-v0-qf34l4milmch1.png?width=1706&format=png&auto=webp&s=e555cb3607a6aa8fc2378aff10ade53fd905827c)

    Is 5.3 Spark broken for anyone else?

- by [unknown](#) **&#x21C5; 1**
  <br/> Yes I’ve not been able to chat to spark since 5.6 release

- by [unknown](#) **&#x21C5; 1**
  <br/> Seems they hardcoded 5.6 input arguments and forgot 5.3 spark uses different ones... As someone who worked as QA Manager, it's baffling how many stupid regression issues OpenAI has. It literally is an automated test to catch these issues, and there's multiple of these with every update.

But I mean I'll cut them some slack, is not like they have a magical AI that can prepare test cases and run them for them.

- by [unknown](#) **&#x21C5; 1**
  <br/> [https://www.youtube.com/shorts/5lsExRvJTAI](https://www.youtube.com/shorts/5lsExRvJTAI)

I'm sorry Dave, I'm afraid I can't do that.

- by [unknown](#) **&#x21C5; 1**
  <br/> I still find it difficult to accurately distinguish between the usage scenarios of "work" and "codex"

- by [unknown](#) **&#x21C5; 2**
  <br/> Big improvement from gpt 5.5 for blender work, still room for improvement but I wasnt expecting to all this, the silo appears to be really nicely done


       [](https://preview.redd.it/gpt-5-6-sol-codex-release-discussion-megathread-v0-gzyossamthch1.png?width=960&format=png&auto=webp&s=2111865db93ecb8e9e1e4dceb606ccccf237bccd)

- by [unknown](#) **&#x21C5; 1**
  <br/> why would gpt 5.5 have improved?

- by [unknown](#) **&#x21C5; 1**
  <br/> Does anybody else still lack 5.6 Sol in Codex?

I have it on ChatGPT Web and in the Classic app, but my Codex/Work app is still limited to Luna and Terra.

- by [unknown](#) **&#x21C5; 1**
  <br/> Yes same here, super weird

- by [unknown](#) **&#x21C5; 1**
  <br/> same for me i tried to update but its not appearing.

- by [unknown](#) **&#x21C5; 3**
  <br/> Sol Max is making more glaring mistakes than 5.5 Xhigh for me. At first I thought I was crazy, but as I was using Sol Max / Ultra throughout the day yesterday, it seems like it was way more likely to miss details, to come up with a problem or solution that wasn't based on the code, and to just generally be less "precise" than 5.5 Xhigh.

This is how I generally feel about Claude models, is that they're a bit more all over the place, more likely to give you an answer without reading all the files or code related to the topic, freewheeling, "creative". Codex has been so good over the last 8 or 9 months at giving high signal/low noise in diagnosing issues, code reviews, etc. and mostly staying grounded in the codebase.

So anyway, I decided to pop back over to Claude Code w/ Fable, and ran this /debate loop skill I'd been using over the last week with pretty good results, where I'd have Fable kick off a codex CLI subagent and then both would in parallel research whatever query I'd fed in, then debate one another over a couple of rounds and come back with the synthesized conclusion.

With 5.5 Xhigh, almost always, Fable would come back and tell me that it was corrected on 2-3 points by Codex, or had new valid issues brought up by Codex that it hadn't flagged.

Which matched my sense of working with the models, Fable seemed more freewheeling, while Codex seemed much more likely to just actually read the files and make conclusions that were grounded in the code.

So I tried this same loop again with Fable and Sol Max, and now for the first time, I'm seeing the reverse. The fable /debate loop comes back now with 3-4 issues that Codex conceded to Fable.

I'm just now working on diagnosing an issue in Prod, and Fable came back with the root cause in 15 mins, Codex took double the time and came back with a hypothesis that was completely different and wrong. It immediately conceded once I pressed it.

I don't know if I'm taking crazy pills or what.

I swapped back to 5.5 Xhigh for a couple /debate loops and again found that Codex was no long conceding points to Fable, instead rather correcting or adding detail again.

Maybe this is just luck at play here, but this model seems sloppier somehow.

- by [unknown](#) **&#x21C5; 1**
  <br/> Did you mean Sol Ultra? It looks like Ultra almost always spawn subagents with lower thinking budget and can actually provide worse results sometimes. Can you try with xhigh instead and see if it makes the same mistakes?

- by [unknown](#) **&#x21C5; 1**
  <br/> GPT-5.6 Sol, Terra, and Luna are available on my work PC, but not on my home PC using the same Codex account

I’m having a strange issue with Codex and can’t figure out what is causing it.

I have Codex installed on both my home PC and my work PC, and I use the same account on both devices. My account has the Pro 20X plan.

When the latest update rolled out, I did not receive the new GPT-5.6 Sol, Terra, and Luna options on my home PC. At first, I assumed the rollout was simply delayed in Europe.

The next morning, I checked my girlfriend’s laptop. She has her own Codex account with a Pro plan, and GPT-5.6 was already available for her.

Later that day, I checked Codex on my work PC. Surprisingly, GPT-5.6 Sol, Terra, and Luna were available there as well. Since both computers use the same account, I assumed the models would also appear on my home PC eventually.

However, they are still missing on my home PC.

So far, I have tried:

Logging out and back in Completely closing and restarting Codex Restarting the PC Comparing the installed app versions on both computers — they are identical Installing Codex through the Microsoft Store Installing it through the website/client Completely uninstalling Codex, including leftover configurations and skills, and then reinstalling it

None of this has fixed the issue.

GPT-5.6 is available for me in ChatGPT through the web browser, so the model is clearly enabled for my account. It is also available in Codex on my work PC. It is only missing from Codex on my home PC.

Has anyone experienced something similar? Could this be caused by a device specific rollout, local system configuration, cached account data, or some kind of server-side device flag?

I’m out of ideas at this point.

- by [unknown](#) **&#x21C5; 1**
  <br/> Update / solved:

I finally found the cause with help from Codex after digging through the local runtime and cache state. It was not an account entitlement issue, and it was not a hidden or disabled flag in the model JSON.

The problem was that Codex Desktop on my home PC was still launching an older embedded Codex app-server runtime, even though a newer Codex runtime was already installed on the machine.

That old runtime kept refreshing the local model cache using an older client version. As a result, the cache was repeatedly rewritten with an older model list that only included the previous models, so GPT-5.6 Sol / Terra / Luna never appeared in the picker.

The confusing part was that I had seen GPT-5.6 references in some local/cache outputs before, but the active runtime that Codex Desktop was actually using kept overwriting the live cache with the old model list.

What fixed it:

  1. Codex helped me check which `codex.exe` process was actually running the `app-server`.
  2. We found that the desktop app was launching an older embedded runtime.
  3. I fully quit Codex / ChatGPT Desktop.
  4. I stopped the old app-server process.
  5. I disabled/renamed the old embedded runtime folder so Codex Desktop could not keep launching it.
  6. I restarted Codex Desktop.

After that, Codex launched the newer runtime, refreshed the model cache correctly, and GPT-5.6 Sol / Terra / Luna appeared in the picker.

Useful Windows diagnostic command:

Get-CimInstance Win32_Process |
  Where-Object { $_.Name -eq "codex.exe" -or $_.CommandLine -like "*app-server*" } |
  Select-Object Name,ProcessId,ExecutablePath,CommandLine |
  Format-List
The important thing is to check which Codex executable is actually running the app-server, not just which version is installed or what the model cache says.
In my case, reinstalling did not solve it because the desktop app kept using an old local embedded runtime. Once Codex identified that stale runtime and I prevented it from launching, the model picker updated correctly.

- by [unknown](#) **&#x21C5; 2**
  <br/> Sol is already at capacity.  Who is seeing these messages?


       [](https://preview.redd.it/gpt-5-6-sol-codex-release-discussion-megathread-v0-g6np35clggch1.png?width=1098&format=png&auto=webp&s=0e90b7505e2965b20c2412069c1cfb6f2277876a)

- by [unknown](#) **&#x21C5; 0**
  <br/> Codex GPT5.6 usage plan on 20x is higher suddely?[](https://www.reddit.com/r/codex/?f=flair_name%3A%22Complaint%22)I received a reset, a bit a go without using the usage resets, but suddenly even with 5.6 Sol at ultra, it is now draining much slower than earlier. Even with /fast enabled.

- by [unknown](#) **&#x21C5; 1**
  <br/> I too feel like this has been updated. 5H limits feel unchanged but my weekly feels more like my 20x.

- by [unknown](#) **&#x21C5; 1**
  <br/> my 5 hour limits seem to have been updated as well, it was eating that shit recently, but after reset i didn't use a usage reset for it seems much more manageable

- by [unknown](#) **&#x21C5; 3**
  <br/> I feel like 5.6 thinks and considers much more, but also does a lot more careless mistakes.[](https://www.reddit.com/r/codex/?f=flair_name%3A%22Complaint%22)This is very anecdotal of course and maybe I am wrong or just have wrong exceptions.

But since heavily using 5.6 Sol (mostly Ultra) now for many tasks, I notices many more small "simple" mistakes, that 5.5 was much more thoroughly with.

I did a longer audit of a current project and it actually went **a lot** deeper on the review of everything – took 30 minutes and wrote a really long highly detailed plan to fix/optimize the findings.

Me expecting a pretty strong reasoning, I did my usual 2-3 Plan check runs with fresh sections and adapted the Plan 2-3 times. After all the different chats feeling confident, I started the implementation with a few manual checks in between.

This is my usual process and with 5.5 xhigh it worked really well for those cases and it never did obvious mistakes, rather smaller specific stuff.

5.6 Sol on the other hand did much better on the details, but got some very obvious weird things completely wrong, that didn't even make sense in the context.

I now noticed this behaviour multiple times, of it being very specific and strong in the details, but as I said before, does some very basic careless mistakes – which I never really had an issue with using GPT 5.5 xhigh.

As I said before, it's very anecdotal and maybe I am just expecting too much, but as a heavy x20 user, I def. noticed this specific behaviour much more often.

Maybe I just have to adapt my prompting, but wondering – anyone else have this experience?

- by [unknown](#) **&#x21C5; 1**
  <br/> I heard some people got a reset, but I still haven’t gotten one today. I got one yesterday but not today. Still showing 50% weekly usage right now.

Edit: just got it about 20 mins later

- by [unknown](#) **&#x21C5; 1**
  <br/> When you spend 1-2 hours thinking about a spec and writing a complex prompt, the most disappointing feeling in the world is when an LLM takes your spec and spits out total junk. Or does 1/20th of the work and then asks if it should keep going.

5.6 Sol Ultra finally - **finally!** - lives up to my expectations here. If it's not done, it knows it, and it keeps going. It just goes and goes until it is highly confident that it has met your expectations.

This is a model for builders, who have really put a lot of thought into exactly what they want and made it clear to the LLM. In the past, even **highly specific, clear-eyed** prompts would go unanswered by LLMs, and you'd have to hand-hold it across the finish line. Now, if you know what you want and tell the LLM what you want, you will get it 90% of the time.

I've been following and using this stuff daily at work and for hobbies since ChatGPT first went public. I used the heck out of Fable. I used the heck out of gpt-5.5 and 4.8 and all the other model shots in the past few years. gpt-5.6 Sol Ultra hits different.

My use cases: Python and TypeScript Lambda functions and Fargate containers at work doing backend cloud stuff, and for hobby, porting a legacy C++ MMORPG to a modern Rust/Linux backend and a Rust/WASM web client. Codebases with hundreds of thousands of SLOC from pre-LLM times. Lots of existing technical debt but functional code. Serious need of rearchitecting, refactoring and modernization across the board.

Sol is delivering shippable code at a rate I've never experienced before with no weird hacks needed to achieve it. It's the closest we've had to "it just works" in agentic engineering to this point. And the usage limits are so high that if you can afford the $200/mo plan, you are basically good to go for serious work.

- by [unknown](#) **&#x21C5; 2**
  <br/> They just reset everyone's quota again didn't they?

- by [unknown](#) **&#x21C5; 1**
  <br/> I can't tell what is a reset, and what is a bug showing my usage at 100%. My weekly usage was at 70% last night, then it was at 100% this morning, then updated back to my previous usage percent of 70%. And now it's at 100% again.

web usage tracker shows it at 100...hopefully it's real!

- by [unknown](#) **&#x21C5; 1**
  <br/> they reset last night and earlier, so it's real haha. nice

- by [unknown](#) **&#x21C5; 1**
  <br/> [](https://preview.redd.it/gpt-5-6-sol-codex-release-discussion-megathread-v0-m8nl76eoofch1.png?width=1920&format=png&auto=webp&s=7310882f76d3e244fa070e6f699473631e71e3fc)

    **I have not had an argument with Codex in nearly 24 hours, and it is glorious!!!**

Been running Codex 5.6 Sol since the announcement, and it is such a step up. I'm basically using Sol Ultra to audit the failures of Codex 5.6, and I swear you'd thinking you were watching a professor grade the work of a mediocre student, which is hilarious.

More importantly, the follow up task is to run a /Goal task to clean up the issues raised in its reports, and then run the audit again. Looping that workflow until it feels that the work is worthy of my review. And for once, the work is finally worthy.

**Side Note:** They are not exaggerating about Sol Ultra burning through credits at insane speeds. I finally had to use one of the 4 rate limit resets I have been saving, and I have already burned through 75% of the limit...in 1 hour! At this rate, those limits will be gone by Sunday morning. Totally worth it.

- by [unknown](#) **&#x21C5; 1**
  <br/> Weird how I have sol but no Terra or Luna. A few hours before I only had Terra and Luna

- by [unknown](#) **&#x21C5; 1**
  <br/> how "resets" are being given? sometimes i have a reset in codex, sometimes not... how many resets are being given each month?

- by [unknown](#) **&#x21C5; 1**
  <br/> [](https://preview.redd.it/gpt-5-6-sol-codex-release-discussion-megathread-v0-ankt2pf2nfch1.jpeg?width=1206&format=pjpg&auto=webp&s=6bb6ed4c7f7681bdec670dafbf1c234684b14314)

    Resets coming.

- by [unknown](#) **&#x21C5; 3**
  <br/> I just got a reset, is that the first one of the day or more to come?

- by [unknown](#) **&#x21C5; 2**
  <br/> We have 1 more.

- by [unknown](#) **&#x21C5; 1**
  <br/> My agents even on ultra mode keep getting this error:"agent thread limit reached" after spawning 3 subagents. I've added this setting to my config.toml:

```[agents]

max_threads = 32

max_depth = 3```

But it's not doing anything to fix the issue. Speaking with chatgpt or codex isn't helping. Does anyone know a workaround?

- by [unknown](#) **&#x21C5; 1**
  <br/> What happened to plan mode?  Shift tab no longer activates it nor does "create a plan..."

Edit:  the keyboard shortcut is now unassigned.  For some reason also typing "plan" does not present the option for me anymore

- by [unknown](#) **&#x21C5; 1**
  <br/> [](https://preview.redd.it/gpt-5-6-sol-codex-release-discussion-megathread-v0-1w1huou8hfch1.png?width=641&format=png&auto=webp&s=d9ca905a44e471801bd15264d821d816da0a465a)

    First day of use.

- by [unknown](#) **&#x21C5; 1**
  <br/> Hi guys, I’m on Pro and Max20, have been using a lot claude lately, and I now have not used a lot of my weekly limits and I have 4 resets in bank.

If you guys have ideas of open source projects (or closed) I can help with by running my gpt codex app using sol ultra on it, let me know!

Cheers

- by [unknown](#) **&#x21C5; 1**
  <br/> Terra Medium is lazy. It'll just take breaks every now and then and call things impossible.

- by [unknown](#) **&#x21C5; 3**
  <br/> I have burned through 60% of weekly usage of 20x plan within an hour... in one sol chat. something is wrong

- by [unknown](#) **&#x21C5; 2**
  <br/> my plus plan burned 20% of my 5h usage in 4 minutes with Terra high.Luna is also very hungry now. I also feel like one 5h usage is a much higher percentage of a weekly reset after that update.

I switched from claude because codex lasted so much longer, I think that´s gone...

- by [unknown](#) **&#x21C5; 1**
  <br/> For my biology bros, will this and have earlier versions sucked ass like Fable with the safeguards?

- by [unknown](#) **&#x21C5; 1**
  <br/> One thing worth watching as people test Sol: prompt compatibility across model versions. If you have workflows built on previous Codex behavior, even small shifts in how Sol handles ambiguity or tool calls can break things in production. The teams that benefit first are the ones with evals that catch regressions fast. Everyone else is just beta testing with their actual projects.

- by [unknown](#) **&#x21C5; 1**
  <br/> Did they just do another reset ?

- by [unknown](#) **&#x21C5; 1**
  <br/> Anyone else STILL not seeing it appear in codex?

- by [unknown](#) **&#x21C5; 1**
  <br/> Have you updated your app? I've had it since at least 5pm yesterday, probably earlier but I didn't check until then. They did say they would be rolling it out over 24 hours so not everyone gets it at the same time.

- by [unknown](#) **&#x21C5; 1**
  <br/> App has updated three times with no new model. Tried logging out and back in. Tried uninstalling and reinstalling. I suspect I’m just part of the last batch.

- by [unknown](#) **&#x21C5; 2**
  <br/> Sol gave up on the task twice, ran through my weekly allowance in an hour, CODEX prompted to change model, changed to Terra - it gave up in the middle stating ‘Selected model is at capacity. Please try a different model.’

Finally went back to 5.5 and got the work done.

- by [unknown](#) **&#x21C5; 1**
  <br/> Maybe I'm one of the last ones to get it cause I rage cancelled for a couple days when shit started to get wonky

- by [unknown](#) **&#x21C5; 1**
  <br/> Not here to talk about tokens

I had a bit of a complex tasks that i was waiting for GPT 5.6 to release to do them  so i decided to use Ultra

Its right  the tasks were complex but not a huge task

For example i wanted to make a compression and encryption algorithm(it would just use AES256 function for encryption) for the backups exported by my app i had already a backup screen and everything works it just produced .sql backups and i wanted to change that , also some other tasks at the same level of complexity or less

I left it for almost 6 hours then came back and i can see its still on the backup task

So i stopped it and asked how much is done it said 3%

After back and fourth it apparently it was making a whole backup platform

Also in the prompt i said (make sure it will also work on MacBook)

The app is electron and already works in macOS i just had some problems previously with "\" and "/" and some scripts and some functions that works only in windows not a big deal

It ended up working 4 hours doing "hardware verifications and signing" and i actually interrupted it because it said this task needed weeks to complete

So i steered it and gave it the correct scope and exactly what it should do and after 4 hours the app is full of errors and its not even confident about what it did and ignored the small tasks

Maybe its my bad i want to hear what you guys think about Ultra mode

- by [unknown](#) **&#x21C5; 1**
  <br/> I feel like this new app is significantly slower than it was before

- by [unknown](#) **&#x21C5; 1**
  <br/> [](https://preview.redd.it/gpt-5-6-sol-codex-release-discussion-megathread-v0-9thnfyw4nech1.jpeg?width=677&format=pjpg&auto=webp&s=5a83895fb3a00013b29b1d0c3cbb6ac1d2ab12fc)

    Codex silently routes to smaller models? Tried to ask both Codex and ChatGPT and getting gpt-5.5 and even gpt-5.4 :(

- by [unknown](#) **&#x21C5; 1**
  <br/> It's hard to say how good Sol Ultra is in terms of code because it consumes the limit like crazy; it seems designed for spending thousands of dollars a month. But what I liked most was how Sol Ultra creates visualizations explaining how everything works.

- by [unknown](#) **&#x21C5; 1**
  <br/> I used one of my reset usage and did not reset my usage what happen here?

- by [unknown](#) **&#x21C5; 2**
  <br/> Just giving you a heads up - the 5.6 [documentation](https://learn.chatgpt.com/docs/agent-configuration/subagents?surface=app#choosing-models-and-reasoning) says that when the models create subagents, they will intelligently decide which subagent model and reasoning effort they will use - however that is not working properly. If you're running Sol high/xhigh and your task creates subagents, the subagents will all inherit the same model and reasoning effort that your main session is using.

I'm assuming this is a bug that will get fixed in time, but this is likely the reason for most of the token burn happening right now

- by [unknown](#) **&#x21C5; 1**
  <br/> Hi,

With the release of 5.6 Sol, for my use case only xHigh seem to be giving me good results, which in turn is causing my 5H limits to get burn quickly. I have a long tasks (ask they Tibo recommends you have to give better/bigger tasks for the new models) which do not complete, which require me to continue once the window resets, but doing so causes cache reset and the model has to go back and relearn everything right, isn't this bad pattern? won't this cause more token burn on the next session? or do i have this wrong?

- by [unknown](#) **&#x21C5; 2**
  <br/> [](https://preview.redd.it/gpt-5-6-sol-codex-release-discussion-megathread-v0-2kleqdvu5ech1.png?width=1385&format=png&auto=webp&s=ae7e674e59e3deaca4f6a22143ec5a718b85da15)

    GPT-5.6 Sol/Ultra burned my entire 5h usage limit + 500 purchased credits on a single read-only audit of an 83k line Python codebase

Built a baseball/softball analytics desktop app (~83,000 lines, solo, no programming experience, using AI assistance). Asked the agent to do a full stability audit — read only, no file writes, no builds, no execution.

Result: 5h limit at 0%, 500 extra credits gone. Weekly limit barely touched (77% remaining), which tells me it wasn't time — it was pure token throughput.

Thoughts?

- by [unknown](#) **&#x21C5; 1**
  <br/> 5.6 Sol Native Subagents Questions  1. Do these subagents use the Sol model too?
  2. Do we know what reasoning level is used?
  3. Are there ways to potentially optimize these things - or are these agents completely beyond user's control?

I find the Sol Ultra setup very impressive as of far.

- by [unknown](#) **&#x21C5; 1**
  <br/> [](https://preview.redd.it/gpt-5-6-sol-codex-release-discussion-megathread-v0-3q2aq0kcwdch1.png?width=461&format=png&auto=webp&s=0fc6db3c39d2482a9a440d18bf28a3c106ab715b)

    I'm afraid to start because it's gonna suck up my weekly limit like Lisa Ann. 💀

- by [unknown](#) **&#x21C5; 1**
  <br/> Hi all,

I jut downloaded the Codex update this morning (I'm on macOS Silicon).The update deleted the Codex app. I also updated the ChatGPT-app (now using version 1.2026.183) which, according to [this article](https://help.openai.com/en/articles/20001275-chatgpt-work-and-codex) should have a built-in Mode Switch to switch between Chat, Work and Codex.But my desktop app does not appear to have such a switch.So, all my codex projects and chats are suddenly gone and I can't do any work.

Anyone experienced this as well? What is going on?

- by [unknown](#) **&#x21C5; 1**
  <br/> Fixed it myself by removing all the ChatGPT apps from my device and reïnstalling them, it now opens Codex and all my projects/chats are there. Phew!

- by [unknown](#) **&#x21C5; 1**
  <br/> This


       [](https://preview.redd.it/gpt-5-6-sol-codex-release-discussion-megathread-v0-ouh4zum5bdch1.png?width=484&format=png&auto=webp&s=24f61048228eb812f2a85be557eb3c751d2ee785)

    Is basically misleading, as web chat is taking Usage too!!!

- by [unknown](#) **&#x21C5; 1**
  <br/> Anyone else have issues while running codex? Computer slows down and mouse cursor lags when I run it, none of these issues in other software/games etc.

This is with the GUI on Windows, not the CLI.

- by [unknown](#) **&#x21C5; 2**
  <br/> What are your feelings towards Sol max ?My feeling is like this keep the execution loop forever. I have a new feature request document and a review report of this document. Then i ask it to revise the document based on the findings from the review report . It then revise this new feature request document and all the other documents in my knowledge base (of existing features). Spend 60% of my 5 hour limit ( pro 5x user) in this loop until i have to interrupt this task. it is like i am using the /goal and entering the loop.Never has this experience with Sol xhigh.

- by [unknown](#) **&#x21C5; 2**
  <br/> Is it just me, or does Sol focus on spawning sub-agents and act as an orchestrator? I'm running constrained prompts to make changes that, with GPT 5.5, wouldn't take more than 10-15 minutes and would normally be executed sequentially. With Terra, it executes sequentially as expected, but Sol, in most cases, refuses to do it itself. It spawns a sub-agent and waits for it to finish, then verifies it, taking significantly longer and easily burning twice as many tokens.

- by [unknown](#) **&#x21C5; 1**
  <br/> Using Sol High inside the Web drains my usage inside Codex too. At least that's what I can see. Any reason? Didn't happen before with 5.5 High.Did they connect the usage as they did with 5.5 Pro Web?

Seems like saving usage is using 5.5 high inside the web and not 5.6 Sol as default on high..

- by [unknown](#) **&#x21C5; 1**
  <br/> I still can't use it yet, guess I'm really unlucky with when the switch for my accout flips the announcment says it may take up to 24h until veryone has it

- by [unknown](#) **&#x21C5; 1**
  <br/> Same here. Are you in EU?

- by [unknown](#) **&#x21C5; 3**
  <br/> my first impression is that gpt-5.6 sol max is an overkill for coding. Should it be used for specifications/planning only?

- by [unknown](#) **&#x21C5; 3**
  <br/> Been trying 5.6-sol today on high. I didn't notice any real difference in understanding or quality, but I DID notice a definite decrease in overall performance. Tasks that would take 30 seconds on 5.5 are taking more than 5 minutes on 5.6. I've gone back to 5.5 now, will try 5.6 again next week.

- by [unknown](#) **&#x21C5; 2**
  <br/> Sol has been on fire finding security gaps and risks in my code base. It is really, extremely helpful, especially since Fable has been completely neutered on that front.

- by [unknown](#) **&#x21C5; 2**
  <br/> Codex auto review is sucking up tokens like crazy, is this normal?

Cloud dashboard says auto review used 700 turns whilst everything else is only at 200.

- by [unknown](#) **&#x21C5; 2**
  <br/> 5.6 Sol Ultra definitely sucks down my tokens far faster than 5.5 xHigh. But I didn't expected anything else. I am still doing code reviews with it. The output seems less abstract and jargon heavy. I'm a dev of over 20 years and sometimes, sometimes I had NFI what 5.5 was saying. Total word salad. 5.6 Ultra appears to be more concrete. Less like a junior dev in an interview trying to impress me.

- by [unknown](#) **&#x21C5; 2**
  <br/> I use Codex in the VS Code extension. I was using Sol on extra high. And then just now I got this error message and Sol has disappeared:


      The 'gpt-5.6-sol' model is not supported when using Codex with a ChatGPT account.


    I don't know what the deal is. I have a paid Plus account. I thought Codex was included in that? Why am I getting restricted and why is it only Sol that's restricted? Terra and Luna remain.

- by [unknown](#) **&#x21C5; 1**
  <br/> is your plan active?, are you able to view gpt 5.6 sol in chatgpt.com?

- by [unknown](#) **&#x21C5; 1**
  <br/> Plan is active and it just came back. I think I just needed to reboot or reset it. It was just a intermittent bug.

- by [unknown](#) **&#x21C5; 3**
  <br/> [](https://preview.redd.it/gpt-5-6-sol-codex-release-discussion-megathread-v0-1lka5phhvbch1.jpeg?width=1578&format=pjpg&auto=webp&s=4f7fe803c2908faeddd9e41f73ab912812009a8c)

    I have tried to Used 5.6 sol ultra in plan mode and used 100% of my 5h and 23% of my weekly usage and did not even finish the plan.

Not complaining regarding the usage cuz it's given that sol ultra will use a lot of tokens but at least finish the plan mode and not give me unfinished photos.Before the prompt: 99%5h and 100% weekly.Used only 1 prompt.

- by [unknown](#) **&#x21C5; 1**
  <br/> What openai plan do you have? Ultra has tendencies to spawn subagents with reasoning ultra as well, that consumes insanelly alot tokens.

- by [unknown](#) **&#x21C5; 2**
  <br/> Sol on high doesn’t feel like 5.5 xhigh with 2x usage I’ll tell you that much. Burned 50% of my pro 5h usage with a single prompt that went for an hour.

- by [unknown](#) **&#x21C5; 1**
  <br/> New 5.6 Luna, terra, sol released.

Can someone explain this to me?

How good is what?

I’ve been seeing people saying Luna Max is better than Terra? Or Using Sol to plan Luna max to implement.

While others saying don’t use Luna use Sol to do everything.

Others saying terra is the best middle ground

Too many choices between model and reasoning and price

How do they compare to 5.5 xhigh also?

- by [unknown](#) **&#x21C5; 1**
  <br/> Running 5.6 sol on high & thinking and it seems like it is a bit slow. Maybe too many people are using it right now.

- by [unknown](#) **&#x21C5; 6**
  <br/> They DESPERATELY need to come up with some sort of “auto” mode for Codex now.

3 models with 5 reasoning levels (6 if you count ultra with sub agents).

How are we to really know when to use what? Like what’s the purpose of Sol on Low? When to just use Terra on High? When to use XHigh? Would Sol on Low be smarter than Terra on Max? Which would be more efficient token usage?

Why can’t the AI itself manage which permutation to use?

- by [unknown](#) **&#x21C5; 1**
  <br/> if an AI was choosing what model to use, it would use the most efficient one and save you tokens. why would a company that sells tokens want to do that

- by [unknown](#) **&#x21C5; 0**
  <br/> You can create your own auto mode, its called creating a good sub agent orchestrator that has rules for when to use which model. Or you can just be like me and use xHigh for everything.

- by [unknown](#) **&#x21C5; 3**
  <br/> Sol Ultra is running on my x20 codex right now.

A yucky start. I have a very complicated — sidecar heavy database. It has all the tools ready available and a well drilled method to import new information into 6 of these sidecars.

I asked it to look at the sidecars, verify and then add a smaller database to the sidecars.

Sol Ultra tried to create a whole new method — which was slower to the order of 3 days slower — then replaced rows without backup — and when I told it to look at the previous methods — it tried to fix its own method based on the already established method rather than use what already works lightning fast.

I’m already fighting with my wife. Now I’m fighting with a know it all — can’t follow procedure AI.

Perhaps Sol thinks it’s smarter than everyone?

- by [unknown](#) **&#x21C5; 0**
  <br/> It needs to build up context. Thats just how it when a new model comes out. Try to get it to reread all the documentation before hand. I always start with a good old audit, not just so it finds issues, but because it creates memories.

- by [unknown](#) **&#x21C5; 3**
  <br/> At this point Sol is just not sustainable for Plus plan, it will wipe limit in minutes. Terra High is probably sweet spot and Luna High I think is also good enough.

If they don't give Plus plan higher limits after GPT 6 coming out, no Plus plan will be able to do any job.

- by [unknown](#) **&#x21C5; 3**
  <br/> Even Sol medium seems like too much for Plus.

- by [unknown](#) **&#x21C5; 2**
  <br/> The model turned out amazing. A 20x plan, a verified passport for cybersecurity, one prompt, and two hours of running 5.6 Sol Ultra at 1.5x speed (it consumed about 60-70% of the 5-hour limit, 15% of the weekly limit) solved a problem I never thought I could solve with version 5.5 in a couple of days, and I wouldn't have been able to do it myself in a couple of months. Thanks to OpenAI.

- by [unknown](#) **&#x21C5; 1**
  <br/> if u verify ur passport u can use it for cyber security?

- by [unknown](#) **&#x21C5; 1**
  <br/> yes, and for many other things, but I use it for cybersecurity. In fact, without verification, models often refuse to do things even remotely related to sensitive topics, verification is a must-have.

- by [unknown](#) **&#x21C5; 1**
  <br/> I’ve got it running right now. 5.5 was pissing me off tonight with codex. Building a website typed what I wanted in chat and it looks like it is making the changes to the site without codex.

- by [unknown](#) **&#x21C5; 1**
  <br/> does anyone know if Codex is able to change the model / reasoning of individual agents while using 5.6 Sol Ultra? it doesn’t appear to be able to do so

- by [unknown](#) **&#x21C5; 1**
  <br/> can’t use sol 😭

- by [unknown](#) **&#x21C5; 1**
  <br/> Anyone still waiting? On Pro plan.

- by [unknown](#) **&#x21C5; 1**
  <br/> STILL waiting. Still. Pro 20x plan. Heavy user.

- by [unknown](#) **&#x21C5; 1**
  <br/> Same
