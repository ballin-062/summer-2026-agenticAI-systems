# Build Journal

One short entry per build — all five Build Challenges plus the smaller daily
builds. Four to eight sentences each: this is a lab notebook, not an essay.
It is also your AI-use disclosure record for the course. Graded on
completeness and honesty about failures, not polish. (50 pts, due Aug 6.)

Template per entry:

## Day N — <build name>
- **What I built:**
- **What failed:**
- **What I changed:**
- **Where AI helped, and how I verified its output:**

---

## Day 1 — Lab 0 (example format; replace with your own)
- **What I built:** connected my Codespace to OpenRouter and ran the end-to-end demo.
- **What failed:** first run rejected my key — I had pasted it with a trailing space.
- **What I changed:** re-ran `bash scripts/set-key.sh` and re-ran the gateway task.
- **Where AI helped, and how I verified its output:** asked the TUI to explain the agent loop; cross-checked its claims against the gateway log lines.

## Day 2 — Mini-Build: Workflow vs. Agent

| Run | Version  | Calls | Tokens | Turns | Score /7 | Notes |
|-----|----------|-------|--------|-------|----------|-------|
| 1   | workflow |   3   |  830   | n/a   |     7    |       |
| 2   | workflow |   3   |  811   | n/a   |     7    |       |
| 3   | workflow |   3   |  820   | n/a   |     7    |       |
| 4   | agent    |   4   |  2543  |  4    |     7    |       |
| 5   | agent    |   4   |  2590  |  4    |     7    |       |
| 6   | agent    |   4   |  2611  |  4    |     7    |       |

Verdict — for THIS task I would ship the (workflow / agent) because: 
Workflow. The number of tokens used is roughly 1/3 the cost of the agent without sacrificing performance. However, I would run more than 3 trials (perhaps 100?) and draw better descriptive statistics across the the runs to get a more accurate picture of performance.
Cost: which version used more tokens, and roughly how much more? 
The Agent used roughly 3 times as many tokens, and the ouput was much more succinct and tight.
Reliability: which scored more consistently across runs? 
Both scored perfected against the rubrik, however the agent was much more compact and tight with it's answers.
One thing that surprised me:
I expected the performance difference to be greater--one or the other would drastically miss the mark.
Additionally, I found it easy to put together the pieces of both the workflow and the agent.
What I had to correct in code my agent wrote (AI-use disclosure — expected, not penalized): 
I had to manually configure my LITELLM_API_KEY environment variable after several retries using the bash scripts provided.
Additionally, the LLM crafted code for the workflow leveraged a TypeError and misused the chat(), so I had to ask Claw to rewrite and debug the error.