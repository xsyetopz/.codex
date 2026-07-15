#Sol Medium as a main driver - Tibo's recommendations [Visit](https://www.reddit.com/r/codex/comments/1utuzrr/sol_medium_as_a_main_driver_tibos_recommendations/)
### **Subreddit:** [r/codex](https://www.reddit.com/r/codex)
### **Author:** [petburiraja](https://www.reddit.com/user/petburiraja/)
### **Vote:** 350
---
Saw this tweet, and wanted to share here.
As my internal tests so far also converged on Sol Medium being optimal main driver, switching to Sol High for more complex/strategic sessions, and using Dol XHigh+ only as ad-hoc advisors.
No optimal use cases were found for Terra and Luna in my workloads all in all (only with Terra Max showing some outstanding results on some tasks).
Routine tasks were recommended to dispatch to GPT Mini or Sol Low instead of Luna during my assesment. Also, I have OpenCode setup of DeepSeek Flash 4 + GLM 5.2 for routine cheap high volume implementations sometimes, which is supervised by Codex. And this cheap combo, I think, is really hard to beat, even with new low cost models, such as Grok 4.5 or MuseSpark 1.1.
I'm curious what optimal model/variants stacks have you guys found for your projects?
And which models/variants you discarded as not optimal across the triangle (intelligence, cost, speed).
---
![Sol Medium as a main driver - Tibo's recommendations](https://preview.redd.it/sol-medium-as-a-main-driver-tibos-recommendations-v0-oxs6igcuvnch1.jpeg?width=640&crop=smart&auto=webp&s=e82218e71b4faead039065cbfc2059f18b4d180b)
---
## Comments 78

- by [unknown](#) **&#x21C5; 108**
  <br/> I actually wish we had a more concrete way to determine which model to use. A "daily driver" could mean anything based on how you "drive"

- by [unknown](#) **&#x21C5; 42**
  <br/> I wish there was a "smart usage" option.

It looks at the complexity of the ask, then chooses the best option. Maybe it molds over time if you tell it the output was too stupid or wildly off.

- by [unknown](#) **&#x21C5; 2**
  <br/> I agree, it's a pain, i feel it's mostly "bad" marketing. I get that for some orchestration you need fine tuning but for a lot of dev tasks just pick the most efficient one when planning or coding i would be fine with that

- by [unknown](#) **&#x21C5; 2**
  <br/> I'm pretty new to using codex but I added a bit to agents.md about recommending which model to use based on my prompt when it begins tasks. So it'll say I should use a different model if it thinks it's needed. Don't have it fully fleshed out yet as sometimes it'll recommend a different model and proceed to work anyway - but it lets me adjust as needed better than before.

- by [unknown](#) **&#x21C5; 2**
  <br/> I did this same thing earlier today and it was a suggestion from codex after chatting a bit with it on the topic lol

- by [unknown](#) **&#x21C5; 2**
  <br/> Cursor auto does this

- by [unknown](#) **&#x21C5; 1**
  <br/> I asked chatgpt about this - doesn't that use API usage, or can it choose from my current claude and chatgpt subscriptions?

- by [unknown](#) **&#x21C5; 1**
  <br/> It doesn’t use API usage when you’re in “auto” mode. I don’t know about choosing from your current subs. I know you can use your API keys from those providers but I’d imaging that uses API cost instead of your 5h window from that provider for example

- by [unknown](#) **&#x21C5; 40**
  <br/> I think Luna XHigh is a bit better, but way more efficient. It is a bit slower though.


       [](https://preview.redd.it/sol-medium-as-a-main-driver-tibos-recommendations-v0-gh8uxkiwwnch1.jpeg?width=1080&format=pjpg&auto=webp&s=3b8a5e06bba201b51b95a883ecab4d0f6ddd32aa)

- by [unknown](#) **&#x21C5; 7**
  <br/> I would argue that Luna xhigh is the best implementer and simple task model but sol medium is a better driver

- by [unknown](#) **&#x21C5; 3**
  <br/> *Simple* Tasks? Luna Light, Medium, High is fine.

- by [unknown](#) **&#x21C5; 9**
  <br/> doesn't that screenshot say that it's *not* token efficient?

- by [unknown](#) **&#x21C5; 11**
  <br/> I should have worded it better, the tokens are obviously cheaper, but yeah it uses more. But it's still a net positive in terms of actual costs.

Edited my original message to avoid confusion.

- by [unknown](#) **&#x21C5; 2**
  <br/> Ah gotcha, that makes sense

- by [unknown](#) **&#x21C5; 2**
  <br/> Probably a stupid question but given.codex plans don't use the exact api prices do we know if the relative usage cost relationship holds? Is luna still 5x cheaper per token on codex?

- by [unknown](#) **&#x21C5; 1**
  <br/> Not sure

Seems like no, though, but it's tough to say

- by [unknown](#) **&#x21C5; 4**
  <br/> It's stupid. It ignored obvious instructions for me and struggles to grasp what I meant, so did terra. Sol medium is like 5.5 . 5.5 always understood and barely ever made mistakes for me.

- by [unknown](#) **&#x21C5; 2**
  <br/> I’ve been using Luna xHigh yesterday and today and have been happy with it. Not quite as token friendly as 5.3 was for me, but soooo much better than 5.4 or 5.5.

- by [unknown](#) **&#x21C5; 3**
  <br/> [](https://preview.redd.it/sol-medium-as-a-main-driver-tibos-recommendations-v0-6liwkz441och1.jpeg?width=1206&format=pjpg&auto=webp&s=aceb1181d9beac1ac4918985094e22a5bca5aa72)

    I asked ChatGPT and this is what it suggested based on specs and cost.

- by [unknown](#) **&#x21C5; 11**
  <br/> From all the benchmarks I've seen, you never really want to use Terra.


       [](https://preview.redd.it/sol-medium-as-a-main-driver-tibos-recommendations-v0-yny519x04och1.jpeg?width=4661&format=pjpg&auto=webp&s=5e56cb640ed11176f8b98cac2a9242d763cad347)

- by [unknown](#) **&#x21C5; 12**
  <br/> Your benchmark says terra max is good.


       [](https://preview.redd.it/sol-medium-as-a-main-driver-tibos-recommendations-v0-si46z5rw7och1.png?width=2058&format=png&auto=webp&s=340a9fd75c6840bb1dfd135a484618f10396a179)

- by [unknown](#) **&#x21C5; 2**
  <br/> My experience with Terra is that it'll fail to solve a task at all pretty often.

These benchmarks more often need rates of hallucination, and rates of insisting it finished a task when it didn't.

For some reason it seems to confidently fail them a lot more than Luna for me in graphics programming. Though I think that's wrong and I just give Luna credit for being much cheaper. [They're both really bad at this](https://i.imgur.com/qxsIQsF.png)

- by [unknown](#) **&#x21C5; 4**
  <br/> Luna is slower, it takes more steps to get to a point, it generates more tokens.

- by [unknown](#) **&#x21C5; 3**
  <br/> Do more tasks at once.

- by [unknown](#) **&#x21C5; 2**
  <br/> that is an option, if my main task is not important enough that I want to finish it faster

- by [unknown](#) **&#x21C5; 2**
  <br/> , it generates more tokens.


    But said tokens are much cheaper.

- by [unknown](#) **&#x21C5; 2**
  <br/> I could be doing something crazy but I’ve done a significant amount of my projects with GPT-5.4-mini up until this point and managed to get decent results.

- by [unknown](#) **&#x21C5; 1**
  <br/> I am on the Plus plan and see in the model selection list below GPT 5.4 "leaving on July 23rd"

Is this a plan specific or company wide retiring of 5.4?

- by [unknown](#) **&#x21C5; 1**
  <br/> They're way too quick to pull older models, and way too quick to push new models to prod.

- by [unknown](#) **&#x21C5; 4**
  <br/> This seems to support Luna as a daily driver since it's "near-frontier coding performance at 1/6 the cost"

- by [unknown](#) **&#x21C5; 1**
  <br/> ChatGPT does not know anything about 5.6.

- by [unknown](#) **&#x21C5; 1**
  <br/> Can you give me a link to this post? Ive been looking for something like this

- by [unknown](#) **&#x21C5; 1**
  <br/> Yeah I got it from here [https://www.reddit.com/r/codex/s/wyNlOkQWxt](https://www.reddit.com/r/codex/s/wyNlOkQWxt)

- by [unknown](#) **&#x21C5; 1**
  <br/> So I'm curious.

Benchmarks typically put Luna Max above Sol Medium while costing less.

Is Sol Medium actually "smarter" and will succeed at tasks that Luna Max fails at? Is there any proof to that? Or is Medium faster or something? Probably so on that one at least and cheaper than running Luna Max Fast.

- by [unknown](#) **&#x21C5; 1**
  <br/> Yes been using sol max for planning and luna max for code, works well

- by [unknown](#) **&#x21C5; 15**
  <br/> I wish more rationale about this advice was included, out of curiosity, but I've been defaulting to medium effort for months now so I think I get it.

Beyond that, the reality is that 99% of people will never be working on "really hard problems". I only bump up effort levels when systems design or algorithmic complexity pushes well beyond the day-to-day.

- by [unknown](#) **&#x21C5; 2**
  <br/> I'd love speed was taken into account, like if Terra is faster than Sol that's quite important.

- by [unknown](#) **&#x21C5; 18**
  <br/> based on the chart im looking at, terra max is actually better than both sol medium AND high


       [](https://preview.redd.it/sol-medium-as-a-main-driver-tibos-recommendations-v0-6j2x8bc4xnch1.jpeg?width=4096&format=pjpg&auto=webp&s=54539bd25d6e11840049cb93c22b755599544d26)

- by [unknown](#) **&#x21C5; 7**
  <br/> Here's another graph going around: [https://artificialanalysis.ai/?intelligence-efficiency=intelligence-vs-cost-per-task&models=gpt-5-6-sol-low%2Cgpt-5-6-terra-medium%2Cgpt-5-6-luna%2Cgpt-5-6-terra-high%2Cgpt-5-6-luna-xhigh%2Cgpt-5-6-luna-high%2Cgpt-5-6-terra%2Cgpt-5-6-terra-xhigh%2Cgpt-5-6-terra-low%2Cgpt-5-6-luna-low%2Cgpt-5-6-luna-medium%2Cgpt-5-6-sol-medium%2Cgpt-5-6-sol-high%2Cgpt-5-6-sol-xhigh%2Cgpt-5-6-sol](https://artificialanalysis.ai/?intelligence-efficiency=intelligence-vs-cost-per-task&models=gpt-5-6-sol-low%2Cgpt-5-6-terra-medium%2Cgpt-5-6-luna%2Cgpt-5-6-terra-high%2Cgpt-5-6-luna-xhigh%2Cgpt-5-6-luna-high%2Cgpt-5-6-terra%2Cgpt-5-6-terra-xhigh%2Cgpt-5-6-terra-low%2Cgpt-5-6-luna-low%2Cgpt-5-6-luna-medium%2Cgpt-5-6-sol-medium%2Cgpt-5-6-sol-high%2Cgpt-5-6-sol-xhigh%2Cgpt-5-6-sol)

Terra Max has more raw intelligence than Sol Medium (less than Sol High), but it also costs more for virtually equivalent results.

- by [unknown](#) **&#x21C5; 2**
  <br/> Yeah, none of the terra models are on the Pareto frontier.

Seams like luna low-xhigh for budget, then sol medium or higher for anything more complex

- by [unknown](#) **&#x21C5; -1**
  <br/> Terra max is the way to go

- by [unknown](#) **&#x21C5; 5**
  <br/> Luna high or Terra medium for me depending.

Luna in general is amazing.

- by [unknown](#) **&#x21C5; 4**
  <br/> I'm literally trying to burn through my weekly usage right now so that I can use the reset before it expires, lol.

- by [unknown](#) **&#x21C5; 3**
  <br/> Where can I reach this guy? They need to add like 3 buttons where I can assign a model+effort+speed preset to each. Having to click 6 times to switch it between questions is bad ux.

- by [unknown](#) **&#x21C5; 3**
  <br/> This is what I've vaguely settled at. Sol Medium seems to be the sweet spot of "clearly better than 5.5, and in some cases, even lower token use", but you have to be pretty specific about exactly what you want - if you give Sol a vague prompt, it'll go off the rails. But if you already have a bunch of context, it's surprisingly fast, and seemingly not that token heavy.

However.... the second you start going into Sol High  or Extra High, jesus christ the tokens lol. And again, if you don't give it very precise stuff, you'll basically hit one of your daily limits in a single prompt.

- by [unknown](#) **&#x21C5; 3**
  <br/> I get they want to give options but all of these models with varying levels is just stupid. Condense it down to a power, pro, economy model and that’s it. Give some charts showing the usage of tokens and make it vary an obvious amount between models. Trying to gamify 15 diff settings is just annoying.

- by [unknown](#) **&#x21C5; 1**
  <br/> For real. Also the naming. I'm happy they wanna get cute with names but I don't wanna have to remember "Sol means XXX and terra means YYYY" when you know for GPT 6 all of that is gonna get thrown out the window and we'll have to learn more dumb names.

Just make it straight to the point. Even 4o / 4.1 / o3 made more sense.

- by [unknown](#) **&#x21C5; 6**
  <br/> xhigh is if you want to close your eyes and just make anything

- by [unknown](#) **&#x21C5; 3**
  <br/> Not quite true yet unfortunately. Just yesterday I had to go through 2 sol max review rounds to fix P1 issues made by sol xhigh implementation.

- by [unknown](#) **&#x21C5; -1**
  <br/> i dont think you understand what i meant, i mean it will just do random shit

- by [unknown](#) **&#x21C5; 2**
  <br/> I've been getting great results so far with Sol low, provided it's following a clear pre-organized plan.

- by [unknown](#) **&#x21C5; 2**
  <br/> NTY. Too expensive for what i need in a daily driver. 5.5 medium was overkill but it ended up being fine and i enjoy how fast it was.

Now we either have sol which ends up using at least 2x, or the lower models which just perform straight up worse unless you set them to high/xhigh/max.

I'm really hoping they tone down sol mediums tendency to go overboard with safeguard steps and checks and make it's task scoping similar to 5.5 medium. Right now it's far too burning. It actually seems slightly better today than yesterday so that's a good sign tbh.

- by [unknown](#) **&#x21C5; 2**
  <br/> I use Sol High to plan, Terra High to implement the plan, Luna High for finishing touches

- by [unknown](#) **&#x21C5; 3**
  <br/> I agree with Tibo, he is such a smart babe.

- by [unknown](#) **&#x21C5; 1**
  <br/> Terra ultra best price per token

- by [unknown](#) **&#x21C5; 1**
  <br/> I was high for daily , medium for repetitive task and Xhigh for complexity

- by [unknown](#) **&#x21C5; 1**
  <br/> IDK but Max feels better than Ultra Sometimes!

- by [unknown](#) **&#x21C5; 1**
  <br/> [](https://preview.redd.it/sol-medium-as-a-main-driver-tibos-recommendations-v0-qp0vrf1ucoch1.png?width=1701&format=png&auto=webp&s=e2552a5cf259689637d7a3c4edfbe428e8cd8185)

- by [unknown](#) **&#x21C5; 1**
  <br/> SolHigh fir me

- by [unknown](#) **&#x21C5; 1**
  <br/> Hey, boss, stop quietly nerfing the limits!!!

- by [unknown](#) **&#x21C5; 1**
  <br/> agreed but my banked reset expires in 2 hours so i am using ultra on fast

in under an hour 50% 5 hour usage is gone . amazing

i will use med but i also do not know how to trigger subagents with sol med

- by [unknown](#) **&#x21C5; 1**
  <br/> Whats the point of the terra then ?

- by [unknown](#) **&#x21C5; 1**
  <br/> This is very generic advice. One-size-fits-all is the opposite of how to use this technology. Experimentation is the way -- find what works for you.

- by [unknown](#) **&#x21C5; 1**
  <br/> It’s surprising we don’t have real adaptive thinking so far. Very confusing to choose between sol medium and Luna xhigh.

Hard for me and the benchmarks  make to out the difference.

There is tons of papers that activate a different percentage of weights each pass and have one model that can act at three different sizes as needed

- by [unknown](#) **&#x21C5; 1**
  <br/> The problem is that Ultra is not “fast”.

So far it’s been physically impossible for it to finish anything in <24 hours. It just endlessly chases nits and continually adds to the to-do list.

- by [unknown](#) **&#x21C5; 1**
  <br/> honestly anything other than ultra so far has been disappointing, else its just hallucinating severely and not correctly understanding me. An app that was ready to ship, i just wanted it to mockup a new design, liked the design and asked to implement it and it completely missed the mark. I reverted back and tried on ultra and never looked back. Sure ultra consumes a lot of tokens but if it one shots more frequently then its worh it to me.

- by [unknown](#) **&#x21C5; 1**
  <br/> So the optimal workflow is Sol Medium driving, Sol High navigating, Luna implementing, Terra advising.At this point, I need an AI agent just to decide which AI agent should choose the right model for my task.

- by [unknown](#) **&#x21C5; 1**
  <br/> this should pop up in the app, been using 5.5 up until a few hours ago, mistakes were made

- by [unknown](#) **&#x21C5; 1**
  <br/> I tried ultra for designing a plan went from 100% usage to 5% in 10 minutes and still didn't generate the plan :'(

- by [unknown](#) **&#x21C5; 1**
  <br/> Joke's on him, I use Luna medium as my daily driver.

- by [unknown](#) **&#x21C5; 1**
  <br/> I love Luna xhigh and am using it as my daily driver. It is only a touch less intelligent than 5.5 medium while being well under half the cost. It is also enabling me to get by on just a plus subscription since I never used more than 50-60% of my weekly usage on pro.

- by [unknown](#) **&#x21C5; 1**
  <br/> I've been using Ultra for everything so far. What's the difference between Ultra and Max when it's not using agents? Is it just the same as Max in that case? The documentation says this:

For problems that reward a greater investment of time and compute, GPT‑5.6 can push beyond this efficient default. max gives GPT‑5.6 even more time than xhigh to reason and explore alternatives, run checks, and revise its approach. ultra goes further by coordinating four agents in parallel by default, trading higher token use for stronger results and faster time-to-result on demanding tasks.

- by [unknown](#) **&#x21C5; 0**
  <br/> Terra ultra best price per token

- by [unknown](#) **&#x21C5; 1**
  <br/> Been using "Hard" for everything. It's perfect

- by [unknown](#) **&#x21C5; -1**
  <br/> I asked chatgpt which model to use. It told me to use terra xhigh for doing, sol for reviewing and fixing. How bad ia this advice?

- by [unknown](#) **&#x21C5; -1**
  <br/> been on sol medium for months and finally feel like i stopped overthinking my model choices the same way i overthink phone plans

- by [unknown](#) **&#x21C5; -2**
  <br/> Sol Ultra Fast everything, only option

- by [unknown](#) **&#x21C5; -3**
  <br/> No use Terra max or Luna max sol medium is literally worst price for perf wtf
