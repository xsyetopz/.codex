#Luna max instead of Sol medium? [Visit](https://www.reddit.com/r/codex/comments/1utrmty/luna_max_instead_of_sol_medium/)
### **Subreddit:** [r/codex](https://www.reddit.com/r/codex)
### **Author:** [joaopaulo-canada](https://www.reddit.com/user/joaopaulo-canada/)
### **Vote:** 47
---
As many of you, I'm also struggling with my quota burn draining absurdly fast when using Sol medium.
So I asked Sol 5.6 extra high on chat and it suggest me using **Luna max**
Is someone here actually using it as a workhorse? Is it decent?
Or should I stick with sol medium, because its just benchmaxxing?
AI ANSWER"
**Yes—the current data genuinely suggests Luna max is the better quota-conscious daily driver than Sol medium.** It is not merely winning a toy coding benchmark.
Artificial Analysis tested a composite of **321 software-engineering tasks** across repository implementation, terminal workflows, and technical codebase Q&A, averaging three runs. Luna max and Sol medium both scored **75**, with nearly identical component results.
Sol medium
Luna max
Coding Agent Index
**75**
DeepSWE
64%
Terminal-Bench
78%
Repository Q&A
**82%**
Runtime/task
**5.2 min**
Raw tokens/task
**5.8M**
So Luna is **not more token-efficient**. It uses about 2.7× as many raw tokens and takes around 50% longer. But Codex charges Luna at exactly **one-fifth of Sol’s credit rate** for input, cached input, and output tokens.
What the benchmark does not measure wellLuna max may feel more meandering: more tool calls, longer reasoning, slower completion, and potentially more supervision. Sol medium is dramatically more concise and faster. The equal score means they finish a similar proportion of tasks successfully—not that the experience is equally pleasant or that their code is equally minimal. Artificial Analysis explicitly warns that equal composite scores can hide workflow-specific differences.
Real-developer reports are still extremely early and mixed, but there are already users switching from Sol medium to Luna xhigh/max specifically because quota usage feels much better; others praise Luna max while acknowledging its tendency to overthink. ([Reddit](https://www.reddit.com/r/codex/comments/1us7fwv/i_gave_gpt54_gpt55_gpt56_sol_terra_and_luna_the/))
My actual recommendation for youDaily driver:  Luna max
Escalation:    Sol mediumUse **Luna max first** for well-scoped implementation, tests, refactors, and autonomous agent loops. Switch to **Sol medium** when Luna fails once, becomes confused, or the task requires architectural judgment.
So yes: **for your priority—meaningfully better than GPT-5.5 medium without destroying the Codex limit—Luna max is currently the most defensible choice.** Sol medium remains the nicer and faster model, but Luna max appears to offer approximately the same completion capability for materially less quota."
Source: Artificial Analysis
EDIT:
Cool chart that better illustrate this post
[](https://preview.redd.it/luna-max-instead-of-sol-medium-v0-ogbwkmyqboch1.png?width=941&format=png&auto=webp&s=c64948be2abd9b813ca362dfc817feacddefbabd)
---
## Comments 67

- by [unknown](#) **&#x21C5; 53**
  <br/> You need to stay within the same model (sol, terra, luna) to keep the cache discount. If you are escalating late in a session from Luna to another model, you will be hit hard with a full cache write rate for a long context.

- by [unknown](#) **&#x21C5; 10**
  <br/> I generally plan with sol medium or high, and leave the md file to Luna max execute.

Still testing though, I don't have a final decision

I was 100% using sol medium, but if it wasn't for these last resets, I'd be out of gas

- by [unknown](#) **&#x21C5; 4**
  <br/> Those damn resets! I was trying to use up all my credit yesterday so I could use one of my 3 saved resets… still tryna get there. All an all, impressive line up we got yesterday. Good luck finding your sweet spot.

- by [unknown](#) **&#x21C5; 1**
  <br/> Is leaving the .md file more token-efficient than asking it to start a sub agent?

- by [unknown](#) **&#x21C5; 2**
  <br/> Sub agents wipe and get a full new cache as well they dont share the parent cache this was disclosed after someone tested yesterday its insane given they now charge for cache writes

- by [unknown](#) **&#x21C5; 1**
  <br/> Terra Max. That way you match what we had with 5.5 xhigh but you’re also getting 100k extra context window more than 5.5, and it’s half the cost.

- by [unknown](#) **&#x21C5; 10**
  <br/> It all’s depends on what you do no ? Luna and terra are distilled ; that means that they might miss abstract patterns, miss some subtleties, but understand and code well most obvious things. I’m doing science work so for me it’s Sol all the way for thinking and reasoning deep, with some Terra and Luna for basic data analysis. ,

- by [unknown](#) **&#x21C5; 4**
  <br/> terra and luna at which thinking level for scientific data analysis?

- by [unknown](#) **&#x21C5; 2**
  <br/> Depends if I expect it to decide/code something or just use a pipeline. If I already decided on the analysis, have a database with a code book, I usually go with Terra High

- by [unknown](#) **&#x21C5; 1**
  <br/> how is terra high usage consumption relative to 5.5? do you have a feel?

- by [unknown](#) **&#x21C5; 1**
  <br/> Id say 30% less or so for my use case ! It depends a bit but is usually more efficient

- by [unknown](#) **&#x21C5; 1**
  <br/> are you on plus or higher sub?

- by [unknown](#) **&#x21C5; 7**
  <br/> for me i use sol max for planning and terra high for implementing. kinda like fable 5 and opus 4.8

- by [unknown](#) **&#x21C5; 1**
  <br/> This is the way

- by [unknown](#) **&#x21C5; 8**
  <br/> 3 times more tokens and 50% longer doesn't seem like a win to me.

Official statement from OpenAI: "There is often a 5-10x difference in token spend between Medium and Ultra depending on how hard the task is.". (source: [https://x.com/thsottiaux](https://x.com/thsottiaux))

So if you don't want to burn a lot of tokens, definitely do not use ultra and problably not max/very high either. And if sol burns too fast, then go to either Terra or gpt 5.5 which have similar benchmark scores and don't go further than "high" effort, in my opinion, unless it is for making plans or doing really important stuff.

- by [unknown](#) **&#x21C5; 3**
  <br/> My goal was to burn quota slowr. It reaches this because it's charged at one fifth of sol price.

Even though Luna max consumes more token and takes longer to run, it reaches same benchmark result as sol medium

Now, regarding the experience.. Yeah, it's slower

- by [unknown](#) **&#x21C5; 2**
  <br/> It's dumb from openAI that now they have a luna max model.. which is a 3 times greater burden on their systems more or less and will generate them less money. All this model madness is just stupid. They should've stuck to one model with low, medium, high and very high thinking mode. This is too much.

- by [unknown](#) **&#x21C5; 4**
  <br/> Switched to Luna max for most tasks and Sol medium for tricky architecture stuff, quota anxiety gone

- by [unknown](#) **&#x21C5; 9**
  <br/> Why nobody talk about terra ? For me terra high is the perfect spot

- by [unknown](#) **&#x21C5; 21**
  <br/> Luna max outperforms Terra

- by [unknown](#) **&#x21C5; 6**
  <br/> Luna max outperforms terra max?

i feel like your statement really isn't great because you dropped the effort level of terra to nothing?

- by [unknown](#) **&#x21C5; 1**
  <br/> Verified against cost + inteligence Artificial Analysis:





              Claim

              Exact live value

              Verdict








                Sol medium

                53.5888 intelligence, $0.31398/task

                ✅ Rounds to 54 / $0.31



                Luna max

                51.2359, $0.20941/task

                ✅ Rounds to 51 / $0.21



                Sol max

                58.8898, $1.03733/task

                ✅ Rounds to 59 / $1.04



    Within GPT-5.6, my corrected recommendation is:

  - Best quality–cost default: **GPT-5.6 Sol, medium reasoning**
  - Best price-first balance: **GPT-5.6 Luna, max reasoning**
  - Best intelligence regardless of price: **GPT-5.6 Sol, max reasoning**

Why Sol medium remains a reasonable “knee”: moving from Luna max to Sol medium costs about $0.10 for three Intelligence points. Beyond Sol medium, marginal gains get progressively more expensive. However, “best balance” is a judgment—not a benchmark fact.

The official [https://artificialanalysis.ai/articles/gpt-5-6-has-landed](https://artificialanalysis.ai/articles/gpt-5-6-has-landed) confirms that Luna and Sol occupy the GPT-5.6 Pareto frontier while Terra trails them. Outside the GPT-5.6-only comparison, Sol medium is not globally optimal: Grok 4.5 high is marginally more intelligent and slightly cheaper.

- by [unknown](#) **&#x21C5; 5**
  <br/> are you a bot? because you literally ignored terra AGAIN

and the guy who this reply is targeted at is talking about terra, not your random ass post

- by [unknown](#) **&#x21C5; 3**
  <br/> Ya probably since Terra Max scores exactly the same as Sol Medium for 1/2 the cost i've noticed people keep trying to push people to sol medium for some reason

- by [unknown](#) **&#x21C5; 3**
  <br/> That claim is bad if your not including Terra Max, Terra max is same score as Sol Medium for HALF the cost

- by [unknown](#) **&#x21C5; -5**
  <br/> It's inferred to be medium from the parent comment. But you seem to have put no effort into thinking yourself.

- by [unknown](#) **&#x21C5; 3**
  <br/> there is literally no mention of 'terra medium' anywhere except your comment...?

so please read everything again and tell me i'm the one doing no effort thinking...?

pie1879 replied to someone saying 'terra high'

the original post is about SOL medium

this pie1879 guy is saying luna max outperforms terra (with no effort mentioned)

does luna max outperform terra high or terra max?  i dont' think so, so saying 'luna max out performs terra' seems wrong

- by [unknown](#) **&#x21C5; 1**
  <br/> Terra high ? In coding ? But what about the rest ? If yo mask something else than coding ?

- by [unknown](#) **&#x21C5; 9**
  <br/> Both are decent, but according to benchmarks, Terra high is just an improved 5.5

Luna max is painfully slow, but achieves a better score if you can wait

That's the TLDR I got here:

Best pleasant daily driver: Terra high

Best capability per quota:  Luna max

Best overall experience:    Sol medium

- by [unknown](#) **&#x21C5; 2**
  <br/> What?? No?

Terra high scores significantly below 5.5, or i guess that depends on what effort you mean by just "5.5".


       [](https://preview.redd.it/luna-max-instead-of-sol-medium-v0-gp357pcxinch1.jpeg?width=1170&format=pjpg&auto=webp&s=33639ffbbae1a4ee519341e67dd2f5e4faed4d0a)

    5.5@medium holds up, but i always found that 5.5 at anything but high was essentially useless.

i would say:

- Daily driver; sol@medium

- by [unknown](#) **&#x21C5; 1**
  <br/> 5.5 medium was usually great. If Terra high can match it for half the price (plus cache write stealth premium) then it might be worth trying.

- by [unknown](#) **&#x21C5; 1**
  <br/> i use sol high (company paid for plus) for plan and prd. 5.5 high from azure for implementation (i have credit) it's fast

- by [unknown](#) **&#x21C5; 1**
  <br/> I’ll use Terra high, or xhigh, to implement a 6000 lines spec sol max wrote. Does it have a reasonable cosumption in regard of limits?

- by [unknown](#) **&#x21C5; 1**
  <br/> Terra Max ties Sol Medium for performance on intelligence, and i believe is faster, for 1/2 the price of input and output,

- by [unknown](#) **&#x21C5; 4**
  <br/> Terra high

              Luna max








                Coding Agent Index

                72

                **75**



                Average time/task

                **6.2 min**

                8.0 min



                Tokens/task

                **5.5M**

                15.5M



                Estimated cost/task

                $1.59

                **$1.57**



                Likely feel

                Direct, responsive

                Thorough, meandering

- by [unknown](#) **&#x21C5; 2**
  <br/> From where this numbers?

- by [unknown](#) **&#x21C5; 2**
  <br/> Artificial analysis

- by [unknown](#) **&#x21C5; 2**
  <br/> Terra seems subpar at both High as well as xHigh, I am not impressed with it.

- by [unknown](#) **&#x21C5; 1**
  <br/> because we have Terra home

- by [unknown](#) **&#x21C5; 1**
  <br/> It is, Terra High is basically the perfect balance between smart, speed and costs.

- by [unknown](#) **&#x21C5; 1**
  <br/> Cause you can have Sol or Luna with same intelligence cheaper than Terra (or better for same price too). Not parreto

- by [unknown](#) **&#x21C5; 1**
  <br/> Terra hallucinates like crazy. Way more than Sol / Luna.

- by [unknown](#) **&#x21C5; 4**
  <br/> Everyone’s ignoring terra medium. Been great for me.

- by [unknown](#) **&#x21C5; 2**
  <br/> I had similar findings check out what I posted here [https://www.reddit.com/r/codex/s/SS4xjmEyea](https://www.reddit.com/r/codex/s/SS4xjmEyea)

- by [unknown](#) **&#x21C5; 2**
  <br/> AM I the only one that Luna Max just isn't an option in Codex? It caps out at Extra High for me.

- by [unknown](#) **&#x21C5; 2**
  <br/> You need go to Settings > Configurations > Model Features to enable Max option

- by [unknown](#) **&#x21C5; 1**
  <br/> same no luna max shown, I'm on the $20 plan right now, maybe on more expensive one?

- by [unknown](#) **&#x21C5; 1**
  <br/> What if I talk/plan with Sol medium and ask it to implement using Luna sub agents?

- by [unknown](#) **&#x21C5; 1**
  <br/> This is roughly what I am doing. Architect is Sol High and implementer is Luna Max. It is working well, but I might try some more experimenting.

- by [unknown](#) **&#x21C5; 1**
  <br/> You sure Luna max brings any extra benefit for the huge amount of thinking tokens? It sounds great to read and say, "Luna Max", but I'm curious if you notice any difference from say, Luna High?

- by [unknown](#) **&#x21C5; 2**
  <br/> Good question, I also try to avoid all the ultra/xhigh cause sometimes they just overthink. I know benchmarks are higher but benchmarks are intentionally hard to solve (otherwise all modern models would make 100%)

- by [unknown](#) **&#x21C5; 1**
  <br/> I'm not a skilled coder so it's hard to say, I'm certainly going to try lowering the thinking level when I get to an easier part of my project. At the moment I'm building the core architecture of a major component so I'm happy to spend a little for safety.

- by [unknown](#) **&#x21C5; 1**
  <br/> I mean you have terra. I used to spam 5.5 xhigh, now terra xhigh, sol xhigh only for problem solving

Everything i used them on feels and looks like an upgrade

- by [unknown](#) **&#x21C5; 1**
  <br/> Yep, this combo is exactly my setup.

- by [unknown](#) **&#x21C5; 2**
  <br/> I'm adding fable as pre merge PR reviews, the goes back to Luna max to fix

- by [unknown](#) **&#x21C5; 1**
  <br/> Codex Team said during the AMA that Sol medium is the best default model to replace 5.5. Others are more like nano/mini (but smarter). Ultra is used to spawn multiple subagents but with the bug (to confirm is still active) they are all started as Sol and then using max tokens (while sometimes could be switched to Luna/Terra but going to be fixed). Depending on your task you might have same results with Luna xhigh than Sol, especially if the task is straightforward and doesn’t require much “thinking”. I’m pro 5x, using Sol xhigh asking without subagents and I don’t have any problems. But using subagents with Sol is destroying my quota in no time. Hope they fix all that soon, try using Sol medium without subagents to see for the moment if better than Luna xhigh.

- by [unknown](#) **&#x21C5; 1**
  <br/> TLDR, this is the cost efficiency region you should take a look and see if it works for you


       [](https://preview.redd.it/luna-max-instead-of-sol-medium-v0-itytg5ug9och1.png?width=1032&format=png&auto=webp&s=0f9187d39d2ed629c7f54a25fe5aa810ad1e853d)

- by [unknown](#) **&#x21C5; 1**
  <br/> [](https://preview.redd.it/luna-max-instead-of-sol-medium-v0-hzthihb7boch1.png?width=941&format=png&auto=webp&s=418ed634089b7400ac979bdb062d88d685f67ebd)

- by [unknown](#) **&#x21C5; 1**
  <br/> Sol max all the way.

- by [unknown](#) **&#x21C5; 1**
  <br/> Anyone try the fast option for Luna?

- by [unknown](#) **&#x21C5; 1**
  <br/> I haven't yet, but you need to check if this token economics will still make sense after it

- by [unknown](#) **&#x21C5; 1**
  <br/> Try Sol low before resorting to lower tier models.

- by [unknown](#) **&#x21C5; -3**
  <br/> Grok 4.5 in Cursor = GPT 5.6 High

- by [unknown](#) **&#x21C5; 2**
  <br/> No thanks, Elon ;)

- by [unknown](#) **&#x21C5; 1**
  <br/> grok sucks not really gpt 5.6 high

- by [unknown](#) **&#x21C5; 0**
  <br/> Nah, use Sol Medium

[https://www.reddit.com/r/ChatGPT/comments/1uszwqq/heres_why_tibo_recommends_using_sol_medium_for/](https://www.reddit.com/r/ChatGPT/comments/1uszwqq/heres_why_tibo_recommends_using_sol_medium_for/)

- by [unknown](#) **&#x21C5; -1**
  <br/> Look at the chart that was posted recently .. DO NOT EVER USE Sol Medium!

Its Basically Terra Max (exact same intelligence score) for 2x the cost, so its either Use Terra Max or jump to Sol High, Sol Medium is a dead model/reasoning level
