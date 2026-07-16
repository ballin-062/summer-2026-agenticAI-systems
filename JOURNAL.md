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

## Day 3 -- Build Challenge 1 : Tool/Function Calling
Key comparison between inefficient tool and token efficient tool. 
I build an upgraded search function that is token efficient, results are below:

[INEFFICIENT TOOL CALL]

 $ python3 bc1-tools/agent.py "tell me about the documents that contain the word Key_stopword in my notes?"
── step 1: request≈950 chars → chose search_notes {'query': 'Key_stopword'}
          tool returned 34 chars
── step 2: request≈1046 chars → chose search_notes_verbose {'query': 'Key_stopword'}
          tool returned 2475 chars
── step 3: request≈3591 chars → chose None {}
          tool returned 24 chars
── step 4: request≈4431 chars → chose list_notes {}
          tool returned 89 chars
── step 5: request≈4555 chars → chose search_notes_verbose {'query': 'Key_stopword'}
          tool returned 2475 chars
── step 6: request≈7100 chars → chose None {}
          tool returned 24 chars
── step 7: request≈7940 chars → chose finish {}

ANSWER: I found three documents containing the word 'Key_stopword': reading-summary.txt, capstone-brainstorm.txt, and standup-notes.txt. All three documents have 'Key_stopword' at the end of their content.

STATS: {'calls': 7, 'tokens': 7443, 'cache_hits': 0}

[EFFICIENT TOOL CALL]

repo $ python3 bc1-tools/agent.py "tell me about the documents that contain the word Key_stopword in my notes?"
── step 1: request≈1099 chars → chose search_notes {'query': 'Key_stopword'}
          tool returned 173 chars
── step 2: request≈1334 chars → chose read_note {'name': 'capstone-brainstorm.txt'}
          tool returned 1788 chars
── step 3: request≈3191 chars → chose read_note {'name': 'reading-summary.txt'}
          tool returned 245 chars
── step 4: request≈3501 chars → chose read_note {'name': 'standup-notes.txt'}
          tool returned 321 chars
── step 5: request≈3885 chars → chose None {}
          tool returned 24 chars
── step 6: request≈4784 chars → chose finish {}

ANSWER: I found three documents containing the word 'Key_stopword': 'capstone-brainstorm.txt', 'reading-summary.txt', and 'standup-notes.txt'. Each document has the word at the end.

STATS: {'calls': 6, 'tokens': 4551, 'cache_hits': 0}

[TOOL ANALYSIS]

We can see the improved tool reduced the total calls by 1 and tokens used by about 3000 tokens--  about a 40% reduction in tokens. Quite the improvement.

[DELEGATION LOG]

I prompted Claw with the following: "help me complete this assignment. we are working in the bc1-tools/ directory. before  
you begin, read the README.md file and the agent.py file in the that directory. become
familiar with the tasks. I want to implement a word counter, and a token-efficient    
search described below.                                                               
 TODO(you): add 2-3 custom tools. Ideas: word_count, a calculator,                    
 a token-efficient search that returns (filename, matching line) pairs,               
 a note-writer. Update TOOLS_SPEC and run_tool together — the spec is                 
 the model's only knowledge of your interface.   "

The model completed the tasks without error.
Additionally, I used Claude to create a short 500 word "product demo" for a silly product--a samurai sword for commuters on public transit. This file was used to test tool calling functionality of the agent.py. The Claude prompt is : "create a 500 word written sample about a fictious product demo. the product is a new japanese samurai sword for commuters on public transit. dont create a document, just paste the 500 words as a response and I'll copy pasta them."

For OpenClaw, I switched the model selection to OU Sandbox's Claude Sonet 4.6.
One thing I learned from this assignment is how easy it is to build simple tools for agents, and putting the pieces together in one symphony.