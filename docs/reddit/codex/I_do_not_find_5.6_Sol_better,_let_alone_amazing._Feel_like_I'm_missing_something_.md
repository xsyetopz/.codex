#I do not find 5.6 Sol better, let alone amazing. Feel like I'm missing something? [Visit](https://www.reddit.com/r/codex/comments/1utskm7/i_do_not_find_56_sol_better_let_alone_amazing/)
### **Subreddit:** [r/codex](https://www.reddit.com/r/codex)
### **Author:** [NovelLurker0_0](https://www.reddit.com/user/NovelLurker0_0/)
### **Vote:** 42
---
Alright I have been testing Sol (and a bit of Luna) in a real-world project that I was building with 5.5. I say "real-word" but it's a game. I've been working on that for weeks now with GPT 5.5 (and a bit of Fable 5) so I feel like testing 5.6 on that would be a fair assessment of progress.
I am not a Banthropic shill, and I've actually been an extensive Codex user since 5.2 but I have to say I'm kind of disappointed. Besides limits running more quickly (but not as much as many claim), I don't see any noticeable upgrade. In fact I feel like I've been more irritated at Codex the past few days than the past weeks with 5.5.
Some noteworthy weird behaviors I encountered with Sol (x)high:
- I asked Sol to design some new set of skills for some heroes and it went on about how what it suggests is great for timings and carefully choosing skills, etc. But here's the thing: the game is a auto-battler, there's nothing in the code that ever alludes to user being able to select skills. And it's actually in the docs that the game is a auto-battler. So, uh...Sol isn't grounding itself first before working?? I never ever had to explicitly ask 5.5 to ground itself.
- Still pretty much terrible at UI. I see no improvement in UI whatsoever. I know this is game UI, but I feel like being this bad at anything not website UI shows how deeply flawed the model is at representing data for users: implementation details, thoughts, weird copy and useless information still bleeds into the UI. Sol added the label "Management enabled" at the inventory window. What does that even mean? Claims implementation is done (yes even with /goal) but I open the UI to see it broken, like some data being offscreen as soon as I scroll. Same stuff as 5.5. I don't see anything that's better.
- Has wrongly claimed a goal to be done. This one I was surprised! That had never happened to me with 5.5 before. The worst that'd happen is the model would still try, no matter what, even if doing it poorly. But here, Sol just decided to outright NOT work on many bullet points of my requests. I hope this is a bug.
- I do not find Sol any "smarter". Just now, I drafted a design of some passive effects for enemies and asked Sol high to implement. It went off and invented a completely new passive system, basically duplicating how passives from heroes work in the game. Alright to be fair, that system wasn't documented (it is now!) but I'd have expected a oh-so-godly Mythos-level model to figure out it has to follow the existing patterns that already exist within a project...
Anyway, I'm not impressed at all. Everyone's talking about Sol being amazing so I felt like I needed to share a more realistic experience with it...Hopefully yours is better. Might depend on what you work on.
On a related note: Opus/Fable 5 is still much better at UI, but everything else seems comparable. Also, they both fail miserably at reproducing a shader from a video or a gif. Both at max effort. Even mythos-like model seems to struggle a lot with vision somehow.
---
## Comments 74

- by [unknown](#) **&#x21C5; 16**
  <br/> the models all have jagged edges of capability so it may not do well on certain things like game UI design.

from a basic web and mobile UI + intelligence perspective, i have noticed an order of magnitude step up for more mainstream knowledge work + personal lifestyle productivity workflows though (i.e., building web/mobile apps and building slides).

my token usage has 10x'd because i've been enjoying the process so much more.

- by [unknown](#) **&#x21C5; 3**
  <br/> I've noticed considerable improvement in Web UI and app UI, but i've ran basic tasks. He sort of gets it right away now.

- by [unknown](#) **&#x21C5; -1**
  <br/> from a basic web and mobile UI + intelligence perspective, i have noticed an order of magnitude step up for more mainstream knowledge work


    That's good to hear but I'm not sure why something like that wouldn't translate to game UI, especially since the UI here is with plain React...

- by [unknown](#) **&#x21C5; 1**
  <br/> so i have noticed that it generates a concept image, perhaps using the GPT image model, before it makes the web and mobile UI. it's possible that is a hack that makes it more limited in scope vs. for example the base model understanding the concept of design more fully.

i am totally guessing though since i'm not an AI researcher.

- by [unknown](#) **&#x21C5; -1**
  <br/> I don't want to sound mean or anything. But the fact that you don't understand why, might even be the reason why you don't have success with it

- by [unknown](#) **&#x21C5; -1**
  <br/> Oh please. Either write a useful comment or bounce.

The UI is React. Js/html/css. Web technologies.If anything, suckling that much shows how artificial the improvement in mobile and "general" web UI is.

- by [unknown](#) **&#x21C5; -3**
  <br/> Maybe because react and css are not good technologies for game ui?

- by [unknown](#) **&#x21C5; 1**
  <br/> What? Many games UI are based on web technologies especially because it's much easier to work with.

Also not sure what that has to do with 5.6 still sucking at UI, even UI based on web techs which it is supposedly better at.

- by [unknown](#) **&#x21C5; 1**
  <br/> They're perfectly fine for game UI, and easier for LLMs to work with than binary formats in other engines.

- by [unknown](#) **&#x21C5; 1**
  <br/> They typically arent great for game UI if you want it to be cross platform and integrate with the 3d side of the game(if its 3d).

- by [unknown](#) **&#x21C5; 12**
  <br/> IDK man just feels like OpenAI does not know how to optimize their Harness, CLI works way better than the GUI, consume less tokens and is actually way faster than the GUI, I got way better results from the Codex CLI, not only mentioning it's on Linux as well.

If your main benchmark is front end work you will be dissapointed, it's not good.

For actual real enginering, building, shipping, it's way better than anything else, even Luna gives me better results than fable in toolcalling and getting context.

btw, not exagerating I get 2x the usage on CLI than with Codex GUI. CLI is also way more token efficient and 2x-3x faster on inference/recieving the inference than GUI.

- by [unknown](#) **&#x21C5; 7**
  <br/> Codex app actually worked for me, But then it got bloated, and now they merged it with chatgpt app. I dont want to see my personal chats on codex man 🤡

- by [unknown](#) **&#x21C5; 1**
  <br/> I have the same worry, seems bloaded and messy, instead of just keeping it separated and organized that's why I started using the CLI, no matter the UI visual benefits it's a freaking unstable mess

- by [unknown](#) **&#x21C5; 2**
  <br/> They've been messing with codex cli lately a bit more than needed, and they messed up some things.

Fir example, 5.5 up to the release of luna/terra/sol was using an experimental subagent spawning system, version 2. They introduced it in I believe, v0.136.0. It was being forced upon us and we were unable to set a v1. (they've now reverted it to v1, the proper one). The v1 makes it for the main agent to be able to spawn specific models with specific reasoning levels, as you'd expect. The version 2 cannot.

Luna can do this (as well as 5.4) -Terra and Sol cannot - they use this experimental version 2 and it's crazy because the maintainer claims experimental version should not be used and they do not accept feedback on it - yet it is forced upon us. I wasn't able to change it in config.toml.

What this means is that if you use Sol, and you want to spawn subagents, it cannot spawn any other than Sol itself, burning through your usage. Even if it could by some chance, it doesn't know how to do it, nor how to set the model version or the reasoning level, because the subagent schema of the v2 doesn't expose any of it.

We've raised an issue on github, [#31097](https://github.com/openai/codex/issues/31097) (alongside many similar ones) and getting some activity on it, but the maintainers aren't acknowledging.

- by [unknown](#) **&#x21C5; 1**
  <br/> Agree, it's a mess but honestly i used it because I get much more usage out of it than using the GUI, also IDK if it's me but inference speed is more reliable and faster in somecases than the GUI, FAST mode in the GUI has a weird glitch when it turn insanely slow.

- by [unknown](#) **&#x21C5; 1**
  <br/> Dude! Thank you for making that comment on fast mode, I typically never use it but yesterday I was trying to get something out and used fast mode and my god not only did it feel super slow, even the thinking looked slow, it obliterated my usage. I’ll stay away for now

- by [unknown](#) **&#x21C5; 1**
  <br/> try it on CLI maybe it works properly then

IMO

the speed goes 1x on GUI, CLI is 2x faster, then CLI+Linux is 3x due to token eficiency and simpler commands than windows, token efficiency while using the CLI on Linux is insane

- by [unknown](#) **&#x21C5; 1**
  <br/> Wow can it be run via WSL or is your whole operating system Linux? (Excuse ignorance for anything I say, I got into this stuff not two months ago)

- by [unknown](#) **&#x21C5; 1**
  <br/> I don't think so, I have never tried tho only on Fedora

- by [unknown](#) **&#x21C5; 1**
  <br/> I don’t know about this, cli gets features later and is a second-class citizen. OpenAI uses the desktop app internally, not the cli.

- by [unknown](#) **&#x21C5; 1**
  <br/> that's what they say to get you to use it

- by [unknown](#) **&#x21C5; 4**
  <br/> I like it but 5.5 in Codex was the wow moment. This feels incremental so far. Prefer Fable as a big picture planner but, 5.6 Sol has still caught some errors from Fable on some quant work I do. It's only been a few days. I need a few weeks to make a judgement.

I'm probably the wrong person to ask because I've been working on only a couple of related projects in quantitative finance, but going really deep. I like how it can handle long running conceptual work, delegate to agents, and just understand immediately what I want and happily chip away.

Yeah it chews limits. I can see myself moving to Terra high and just using it like 5.5 after using banked resets and pulling Sol out for planning and reviews.

- by [unknown](#) **&#x21C5; 10**
  <br/> for what i do which is basic python coding i dont see much of a difference. 5.5 did what i told it to do, 5.6 also does what i tell it to do. the step up was marginal in my case.

- by [unknown](#) **&#x21C5; 6**
  <br/> 5.5 was already an SOTA model itself, 5.6 is not going to be path-breaking, of course you will not see any improvemnt in python coding capabilities, because they were already very good at it

- by [unknown](#) **&#x21C5; 3**
  <br/> In my domain (specific automation cases where many hardware-software relationships are vendor locked) 5.6 SOL is significantly better. It figures out how to use new software itself much more intuitively, is better at sorting through it extensively, and seems to search RAG databases more effectively across thousands of markdown files that describe individual specific software actions.

- by [unknown](#) **&#x21C5; 3**
  <br/> We've simply reached a point where comparing 2 models to see which one is smarter is like comparing two humans to see which one is smarter... you really can't. It will depend on many factors, such as domain, for one. And the output is often sufficiently complex that you can't downright say one is categorically better.

- by [unknown](#) **&#x21C5; 2**
  <br/> Depends on the domain. For somewhat simple work the difference is negligible. I used to debug an application that injects DLL, patches binaries, and required skilled reverse engineering, and at this point I was totally shocked to the point of disbelief, how good (5.6 Sol Ultra). IDA Pro, x64dbg, objdump, procdump, etc, with ease it handles those utilities. Still, I believe the efficiency of terminal use has long way to go.It requires precise steering still, but if you have good domain knowledge, it’s a monster, I’m afraid what will be the capabilities two-three years from now. As it was said somewhere, it doesn’t add skill, but surely multiplies it. I feel now I have to know and learn a lot-lot more than before.I wouldn’t let it write the code from scratch, though.

- by [unknown](#) **&#x21C5; 2**
  <br/> I am having a horrible experience with it, so much so that there might be some config problem for codex on my system. It lies, fails at any form of complex task and analysis and often it simply abandon tasks with no explaination given. Then the token usage is embarassing, i somehow managed to burn through 82% of my weekly quota in one night (and all that work went into a horrible result that i couldn't use).My theories are currently 2- my setup is broken for some reason- the type of work and projects i ask him to work on make the very big problem the model has with hallucinations more prominent.  (In artificial analysis "Rate of avoiding hallucination among non-correct responses" score is brutally low compared to anthropic models with which i have 1/10th of the problems lately)

In general, i was super hyped for the launch but got letdown big time.

BUT luna, luna feels special in its own way

- by [unknown](#) **&#x21C5; 2**
  <br/> Yeah I feel the same. Sol over engineered every demands that I asked. So I started using Terra xhigh that is supposed to be pretty much similar to 5.5 high, but it was not as good. I think I will stay with 5.5 high for now.

And the model selection with all the thinking efforts are just so damn confusing.

Meanwhile I tried Grok 4.5 the last few days and it felt amazing. Like a faster 5.5 high. But I won’t subscribe to grok or cursor, ChatGPT Plus has a much better value.

- by [unknown](#) **&#x21C5; 2**
  <br/> im working on a project that uses a simple synthesizer built into the code to play sounds. both 5.5 and the new 5.6 sol have no idea what to do with this feature and often "optimize" it by lowering the audio quality without me asking. Claude is far out on top able to understand exactly whats going on. I think gpt is far behind in many ways when it comes to these sort of divergent ideas

- by [unknown](#) **&#x21C5; 5**
  <br/> I mentioned it before - 5.6 is not a revolution, merely an evolution. It still isn't as smart as Fable, which is a proper revolution.

The main difference is that OpenAI can actually serve 5.6 at scale. I think Anthropic has problems serving Fable at scale at the moment, hence all the restrictions on usage.

- by [unknown](#) **&#x21C5; 1**
  <br/> Okay beyond the benchmarks, what makes you think that 5.6 sol is not on par with fable ?

- by [unknown](#) **&#x21C5; -3**
  <br/> OpenAI had a bad pretrain they were going to do with GPT 5. Basically 4.5 was their failure.

This failure gave Anthropic time to catch up… OpenAI needs a radically better pretrain to catch up to Anthropic. They may or may not succeed, but 5.6 is not it. Better post train at the most.

- by [unknown](#) **&#x21C5; 1**
  <br/> In my experience, 5.6 is significantly better than Fable, actually.Not to mention much, much cheaper.Aside from UI, of course.

- by [unknown](#) **&#x21C5; 0**
  <br/> Yeah, there is no way this is true at all. Just ask 5.6 to review literally any of Fable's work. Fable is really good at convincing you that it did a stellar job and everything works end to end with no problem. But trust me, just do one 5.6 review on any of what Fable does and you'll see what I mean. It is absolutely brutal.

- by [unknown](#) **&#x21C5; 3**
  <br/> Yeah, this is a funny model, it can go back and forth between feeling like a big improvement and terrible randomly. In one repo, it's been churning on a plan for like 10 hours when I thought it would have knocked out everything in an hour. All of the supposed token savings means nothing if 50% of the token usage is misaligned behavior or it having poor user intent understanding.

- by [unknown](#) **&#x21C5; 2**
  <br/> i agree with you, its ui decisions are terrible, not even sol ultra can figure it out by themselves that equip needs an unequip option, if i wanna make a 3rd person game 1st person i need to tell it the toggles have to work both ways. Maybe I got lazyer and my prompts but I do expect a "cutting edge" model to recognize UI 101 and act like it. Absolute trash.

- by [unknown](#) **&#x21C5; 0**
  <br/> I Make a Game no Problems with that die you have Skills, Workflows , adrs and so on ?

- by [unknown](#) **&#x21C5; -3**
  <br/> the fact that you are using sol ultra for ui tells me everything I need to know use 5.6 luna its just as good or better than sol for frontend

- by [unknown](#) **&#x21C5; 1**
  <br/> try ultra effort with automatic task delegation

- by [unknown](#) **&#x21C5; 3**
  <br/> ultra is just high or xhigh, it's not an effort level, just a coordinator and burns sooo many tokens.

- by [unknown](#) **&#x21C5; 2**
  <br/> tokens go brrrrrr

- by [unknown](#) **&#x21C5; 1**
  <br/> It's much better at very long running tasks. i.e. Mine just completed a 20 hour job writing some code. I wrote a loop in markdown and it grinded away for almost a day.

I think in your example its actually better to ask it advice for how it should work through long tasks, when it should pivot or stop and ask for clarification. its default behavior is to pivot until something works, which makes sense since it has been tuned from user data and most users don't read code anymore. we also should not assume it will read you're entire project into context, you need to direct it.

- by [unknown](#) **&#x21C5; 1**
  <br/> It's biggest issue by far, for me, is not only overengineering, but even sidestepping the guardrails i attempt to put up to constrain it. It have the source of a sister application in the directory but it instead decides to decompile an existing jar to reverse engineer its own, broken, source code to read... yes I have a repo map setup and I pointed it to the source code in the prompt.

- by [unknown](#) **&#x21C5; 1**
  <br/> I asked it to review my geochemical work that was being performed by Claude Opus 4.8 earlier.

Claude reviewed the work several times , even on ultrathink mode, and always said that the model looks good.

I asked Codex Sol to review it and it highlighted 8 different issues that Claude missed.

When I provided Claude with all these eight issues, Claude verified them and agreed that these are severe issues.

- by [unknown](#) **&#x21C5; 1**
  <br/> it definitely takes some getting used to

as i used it more, i realise how insane it is

- by [unknown](#) **&#x21C5; 1**
  <br/> This is the first time I’ve been able to feed a model a screenshot of one of my agency’s designed webpages and it just one shots it.

- by [unknown](#) **&#x21C5; 1**
  <br/> {"comment": "Sol acting like a lazy intern who claims they finished but did nothing is way too real"}

- by [unknown](#) **&#x21C5; 1**
  <br/> For game dev i found it helps to have a chat about your game design in the various bits and have it write it down in some md files that it can reference later to keep it consistent and in line with your vision.

- by [unknown](#) **&#x21C5; 1**
  <br/> Horrible, horrible, and horrible. Top 3 words to describe these new models... they are somehow even worse than 5.4 at C++, what was the point of hyping it up so much?

Edit: I will give credit, on web stuff that I asked it to build around my app -- it did perfectly, pretty much one-shot, although C++, has me in shock on how much it can downgrade from 5.5..

- by [unknown](#) **&#x21C5; 1**
  <br/> Hey funny enough I feel the same and I'm using it to code Lua for a Warcraft 3 mod/map im making haha... I've had such a blast over a month with 5.5 high, on my end even UI was going well (but WC3 is very simple) - Since 5.6 I am losing patience a bit... what was a fun process has become taxing and I'm still not certain if the issue is how I use Sol or just it's worse.

I do a mix of drafting on ChatGPT and then using Codex as on the regular pro tier I tend to finish my weekly just about - so to save credits sometimes i'll draft in ChatGPT, oddly - I feel like Chat is much better now than before.

- by [unknown](#) **&#x21C5; 1**
  <br/> I've never found codex to be great at design, but I likenit better for coding

- by [unknown](#) **&#x21C5; 1**
  <br/> It's not better. It's the same model with a few tweaks.

I've tested it extensively on three projects of different complexity and I ran into IDENTICAL issues that I've been having for months now.

This is same like it was with Opus 4.6, 4.7 and 4.8. They all did the same mistakes...

- by [unknown](#) **&#x21C5; 1**
  <br/> My recommendation would be to learn about harnesses, grab a couple of templates off GitHub and try again. Looping an agent, with a clear reward metric, iterating, getting it to review failure conditions, is a game changer.

- by [unknown](#) **&#x21C5; 1**
  <br/> Very poor reasoning and attention to [agents.md](http://agents.md) and project docs. At the end better advice is from gpt 5.5 at least for now. Lazy model and because of that, wrong advices, misleading. Hopefully they will tune it.

- by [unknown](#) **&#x21C5; 1**
  <br/> It's very good, but it's not AGI yet.

- by [unknown](#) **&#x21C5; 2**
  <br/> LLM with Transformer will never become or achieve AGI, u know

- by [unknown](#) **&#x21C5; 0**
  <br/> That's your opinion (and lecun's), doesn't make it right, plus it doesn't really matter if agi comes from a LLM or another kind of architecture, it will come anyway.

- by [unknown](#) **&#x21C5; 1**
  <br/> LLMs can never ever become AGI. Just ask gpt 5.6 sol or fable 5 if you trust them and they will say the same I.e humans still don't even have any tech yet that can pave the way for AGI. We may never reach AGI in our lifetime is a very solid probability

- by [unknown](#) **&#x21C5; -1**
  <br/> A very solid probability calculated by you?

Anyway i asked sol ult and it said:

Yes—possibly, but probably not as a “bare” LLM.

A sufficiently advanced LLM could become the central reasoning component of an AGI system, combined with:

  - persistent memory and continual learning
  - vision, audio, and real-world grounding
  - planning, search, and tool use
  - reliable self-checking
  - long-term goals and autonomous action
  - strong safety and alignment mechanisms

I cut the answer short to put it on reddit without using too much space.

- by [unknown](#) **&#x21C5; 1**
  <br/> bro we have actually reached the limits of RL. Everything that is now being shilled to us is just more subagents, meaning more work gets done. I don't think this model is an improvement over 5.5, but it can run for a long time, which is not the feature most of us want

- by [unknown](#) **&#x21C5; 1**
  <br/> i dont think its a secret that 5.6 is not a new model on newly trained data and that it was largely harness and other incremental improvements that does translate into more throughput and addresses the issues that 5.5 had

lacking in the UI department was a given and expected

my main issue is how quickly it burns through your weekly usage. I've used it for 24 hours and i've already ripped through two resets. five hour limits are reached in under 2~3 hours and each time it does it uses up 15~25% of your weekly usage.

note that i am using 5.6 ultra with the config toml hack that was suggested a while back which doesn't seem to do anything

$200/month plan since September but i've never seen codex rip through usage limits this aggressive and fast

now if this was something on the level of Fable 5 ? I'd be more than happy to accept the costs

I have like 2 more banked reset remaining and I dont even know if I'm going to have enough usage by next Wednesday

- by [unknown](#) **&#x21C5; 1**
  <br/> I dont see my resets anymore. Anyone else lose their reset option?

- by [unknown](#) **&#x21C5; 0**
  <br/> So, big disclaimer: I havent been able to use any of them in codex yet.

But looking at both the prices, and the deepswe results. I dont get how Sol are giving yall less usage?

Are you using it at max or what?

At least for the trials used by deepswe, xhigh vs max produced 0 improvements in results, but the price difference was almost 100% higher for max.

Sol@medium seems to be about 1:1 with gpt-5.5@high(which has always been the recommended effort for coding, idk why people keep forcing in xhigh when it clearly performs worse)

But at like 1/4th the cost.. While sol@high is meaningfully better at 1/2 the cost ish.

Ofc i havent tried myself, so its possible that the usage amount itself is reduced.

If you use more than what is it? 270k? 290k? tokens of context the price is 2x, so that ofc would affect things

- by [unknown](#) **&#x21C5; 3**
  <br/> I think it’s because it’s much more thorough. My requests definitely take longer than they did with 5.5, and it seems to verify its own work much more carefully. To me, 5.6 SOL Medium feels roughly like 5.5 at xhigh with a very thorough prompt, while 5.6 SOL High feels a bit excessive.

- by [unknown](#) **&#x21C5; 1**
  <br/> You are right 5.6 sol high consumes less than 5.5 high on plus plan (real world use here)

- by [unknown](#) **&#x21C5; 2**
  <br/> [](https://preview.redd.it/i-do-not-find-5-6-sol-better-let-alone-amazing-feel-like-im-v0-qh693cpgjnch1.jpeg?width=1170&format=pjpg&auto=webp&s=85623ce33251d4e6905756cecbaaf8f953cc4875)

    Sol@medium also is like 1:1 with 5.5@high, but the price difference here might be the most significant out of all

- by [unknown](#) **&#x21C5; 0**
  <br/> You should work on harder problems

- by [unknown](#) **&#x21C5; 1**
  <br/> There is nothing new here..gpt is gpt , for fun its good, for work..nope its definitely will tell you a story about some restrictions and thats it. Basically a nice toy 🪀🧸

- by [unknown](#) **&#x21C5; 0**
  <br/> 5.6 Ultra Terra or Sol on big projects is pretty amazing, for small projects GPT 5 from alst year was more than sufficient

- by [unknown](#) **&#x21C5; 4**
  <br/> Means something that is actually used on a daily basis, not a one-off useless task or another benchmark.

- by [unknown](#) **&#x21C5; 2**
  <br/> I think it was pretty clear from the OP what "real world" meant.
