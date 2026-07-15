#Does sol avoid pathological monolithic files better than 5.5? [Visit](https://www.reddit.com/r/codex/comments/1uu1vb0/does_sol_avoid_pathological_monolithic_files/)
### **Subreddit:** [r/codex](https://www.reddit.com/r/codex)
### **Author:** [shockwave6969](https://www.reddit.com/user/shockwave6969/)
### **Vote:** 0
---
I usually have to refactor my codebase every few days since 5.5 would just let debt build up and monoliths form. Is sol better than 5.5 at managing this so you don't have to refactor as often? What's your experience so far?
---
## Comments 2

- by [unknown](#) **&#x21C5; 1**
  <br/> I wouldn’t rely on the model to notice the boundary by itself. Put a max file size and module ownership rule in [AGENTS.md](http://AGENTS.md), then make the task stop when it would cross one. Sol can follow a boundary; it can’t invent your architecture.

- by [unknown](#) **&#x21C5; 1**
  <br/> You could just incorporate the cursor thermonuclear code quality review skill at the end of each run.

I've even incorporated a "code health ratchet" that tracks several metrics like lines of code per file and fails CI/Tests if health gets worse, and resets the limits if it gets better.

You should be thinking more about this and not rely on the agent to do stuff you didn't tell it to.
