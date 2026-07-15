#GPT-5.6 Sol vs Terra vs Luna: my early guide to choosing the right model without burning your limits [Visit](https://www.reddit.com/r/codex/comments/1utzi5w/gpt56_sol_vs_terra_vs_luna_my_early_guide_to/)
### **Subreddit:** [r/codex](https://www.reddit.com/r/codex)
### **Author:** [emir_morris](https://www.reddit.com/user/emir_morris/)
### **Vote:** 24
---
After two days of heavy coding, switching between the new models, and reading other users’ early experiences on Reddit, this is my current summary.
My goal was to understand how to use the strongest model when it actually matters, without burning through my Codex limits on normal tasks.
This is my current setup:
**Task**
**Model**
Commits, renaming, spacing, tiny UI changes
**Luna Medium/High or GPT-5.4**
Normal bug fix or a clearly scoped feature
**Luna XHigh**
Unclear task that requires exploring several parts of the repo
**Terra Medium**
Complex bug, architecture, auth, payments, migrations
**Sol Medium**
Terra/Sol Medium failed
**Sol High/Max**
Sol Ultra
**Basically never**
My experience so far:
**Sol** is clearly strong, but it burns tokens ridiculously fast. I only use it when the task is genuinely difficult or a bad implementation could cause serious problems.
**Terra** is good, but it has been using more of my limits than I expected. On some tasks, it feels like it burns noticeably more than GPT-5.5, so I don’t think it makes sense as my default model.
**Luna** currently looks like the best option for everyday work. It’s cheaper and seems good enough when the task is clearly explained and reasonably limited.
So my current workflow is:
**Luna XHigh → Terra Medium → Sol Medium**
I only escalate when the previous model actually struggles. Starting every task with Terra or Sol seems like a waste of quota.
This is still based on only a few days of use, plus early feedback from other Reddit users. But for now, **Luna XHigh looks like the best daily driver for me**.
What setup is working best for you so far?
Share which model you use for simple, normal, and difficult tasks. It would be useful to turn the comments into a practical community guide for both new and experienced Codex users.
---
## Comments 23

- by [unknown](#) **&#x21C5; 9**
  <br/> [](https://preview.redd.it/gpt-5-6-sol-vs-terra-vs-luna-my-early-guide-to-choosing-the-v0-3hnbn6xe0pch1.png?width=1532&format=png&auto=webp&s=81e041b068fda09e168763658df7e44ccdbc46ce)

    This is my config now run with sol as orchestrator. basically skipping all of the terra but i don't dare to go luna xhigh for now, usually theyt hink too much on xhigh

- by [unknown](#) **&#x21C5; 2**
  <br/> Did you make this sub-agent yourself? If it's a published/publicly available one, I'd like to know where to get it!

- by [unknown](#) **&#x21C5; 1**
  <br/> yea i did make this myself i tell  GPT to do it based on my usage patterns.

[https://github.com/hindraxxx/subagents_configs](https://github.com/hindraxxx/subagents_configs) i do have installable file so i can share it to my friend but it hasn't been tested yet.

do notes that i introduced an additional SUBAGENT_ROUTING.md that's imported inside the [AGENTS.md](http://AGENTS.md) so that by default my agent always uses this smaller subagent to reduce my token usage. Feel free to take reference/ use the installer above

- by [unknown](#) **&#x21C5; 17**
  <br/> i jus use sol xhigh on 5x and then lwkey go on twitter to complain.

- by [unknown](#) **&#x21C5; 8**
  <br/> "tibo wen reset"

- by [unknown](#) **&#x21C5; 1**
  <br/> Yap that seems like a lot of people work flow, sol ultra then post on Reddit or X, Tibo when reset. Wait 1 hour, get nothing just bitch posting about how OpenAI is scamming you.

- by [unknown](#) **&#x21C5; 4**
  <br/> > Unclear task that requires exploring several parts of the repo

I ran a single (n=1) benchmark and this is what stood out to me the most. Terra used a lot more tokens than the other two but it also found a lot more issues. Sol was the winner on being both a strong model and token efficient. Due to that I use Sol low for the most part. It more expensive but it uses less tokens so its not more expensive.

So for me its

- Sol low as a smart default- Terra for exploration- Luna for edge cases and small tasks

I don't see Terra as less expensive. Its just different. Half the cost but using 2 times the tokens isn't cheaper. Having a different model is great for parallel agents because they're going to behave differently and go down different paths. Deploying all three for deep search is great.

- by [unknown](#) **&#x21C5; 2**
  <br/> I’m starting to think “difficulty” is the wrong axis. I’d rather escalate based on blast radius: a hard but isolated refactor can stay on Luna, while a simple auth or config change might deserve Sol.

- by [unknown](#) **&#x21C5; 1**
  <br/> That’s a good point. Cost per token and cost per completed task are definitely not the same thing. My experience with Terra was similar — it explored much more, but also burned far more of the limit. I haven’t tested Sol Low enough as a default yet, so I’ll try it on a few normal tasks and compare it with Luna XHigh. What kind of task did you use for the benchmark, and which reasoning levels did you compare?

- by [unknown](#) **&#x21C5; 2**
  <br/> It was a code review on a PR. Checked for correctness and other stuff that Sol recommended checking.

All low effort. They all had one issue they found in common and they all found issues the others didn't. I think running all three at the same time would produce really good results for code reviews.

Speed             Luna > Sol >>> Terra

Token efficiency  Sol > Luna >>> Terra

Focused review    Sol

Broad tracing     Terra

Distinct edges    Luna

Compared with Sol:

  - Luna finished about **14% faster**.
  - Luna used about **66% more tokens**.
  - Terra took about **2.6 times longer**.
  - Terra used about **2.9 times as many tokens**.

- by [unknown](#) **&#x21C5; 2**
  <br/> Sol Ultra when you have 1% usage left, you know what to prompt 😉

- by [unknown](#) **&#x21C5; 3**
  <br/> It will still eat up your weekly limit. Tho, it bypass the 5-hour.

- by [unknown](#) **&#x21C5; 1**
  <br/> Haha. It works only for 5h limits

- by [unknown](#) **&#x21C5; 1**
  <br/> I already knew this but wasn't sure can you explain ?

- by [unknown](#) **&#x21C5; 2**
  <br/> Estou usando no direito para redigir peças processuais.

O luna no máximo consegue analisar bem processos e organizar documentos para protocolo, o sol ultra consegue redigir petições complexas de temas extremamente avançados sem precisar de qualquer correção.

- by [unknown](#) **&#x21C5; 2**
  <br/> If you are to believe the Artificial Analysis benchmarks on capability vs cost, There doesn't seem to be a place for Terra. Luna xhigh or Sol on the lower thinking basically close the gap. It was posted in one of the AI Reddits but I'm too lazy to go fetch it.

- by [unknown](#) **&#x21C5; 1**
  <br/> I had a similar finding and shared my workflow here [https://github.com/Jogan/soluna-workflow](https://github.com/Jogan/soluna-workflow). I'm using Sol Low as my driver.

- by [unknown](#) **&#x21C5; 1**
  <br/> Sol on low reasoning is the sweet spot for me, does what I need without eating quota like the higher tiers

- by [unknown](#) **&#x21C5; 1**
  <br/> I dont use it heavily because I cant 2-4 prompts and I have to wait 5 hours

- by [unknown](#) **&#x21C5; 1**
  <br/> Terra medium has been fine for me token wise.

- by [unknown](#) **&#x21C5; 1**
  <br/> I’m driving with sol daily, because my code is complex, Terra and Luna eat up way more usage than sol, just trying to figure out what they’re looking at

- by [unknown](#) **&#x21C5; 1**
  <br/> Sol ultra and max only.

- by [unknown](#) **&#x21C5; 1**
  <br/> With my resets left I’m struggling to max out my usage before they expire. Running 4 projects on sol high currently in parallel. 2.5 hours left and I’m at 25% of weekly still remaining.
