#!/usr/bin/env python3

import os
import re
from common.llm import chat, STATS

# Base directory: resolve all file paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


# ── Tool functions ────────────────────────────────────────────────────────────

def read_notes() -> str:
    """Return the text of notes.txt located next to this script."""
    path = os.path.join(SCRIPT_DIR, "notes.txt")
    with open(path, "r") as f:
        return f.read()


def count_items(text: str) -> str:
    """Count action items in text by counting non-empty lines that look like list entries."""
    lines = [l.strip() for l in text.splitlines()]
    count = sum(
        1 for l in lines
        if l and (l[0] in "-*•" or (len(l) > 2 and l[0].isdigit() and l[1] in ".):"))
    )
    # Fall back to counting non-empty lines if no bullet/numbered lines found
    if count == 0:
        count = sum(1 for l in lines if l)
    return str(count)


def save_output(text: str) -> str:
    """Write text to agent_output.txt next to this script and return 'saved'."""
    path = os.path.join(SCRIPT_DIR, "agent_output.txt")
    with open(path, "w") as f:
        f.write(text)
    return "saved"


# ── Tool registry ─────────────────────────────────────────────────────────────

TOOLS = {
    "read_notes": read_notes,
    "count_items": count_items,
    "save_output": save_output,
}

TOOL_DESCRIPTIONS = """
You have access to exactly three tools. Call them using this exact format:
  ACTION: tool_name(argument)
For tools with no argument, use: ACTION: tool_name()
For tools with a text argument, pass the text directly (no extra quoting needed).

Tools:
  read_notes()           — Returns the full text of notes.txt.
  count_items(text)      — Given a block of text listing action items, returns the count of items.
  save_output(text)      — Writes text to agent_output.txt and returns "saved".

When you are completely finished, reply with:
  DONE: <your final answer>
"""

SYSTEM_PROMPT = f"""You are a meeting-notes analyst.

GOAL:
1. Read the meeting notes.
2. Extract every action item as a list of: task | owner | deadline.
   Use MISSING when an owner or deadline is not stated.
   Ignore ideas that were explicitly parked.
3. From that list, identify items that have a MISSING owner or deadline.
4. Write a 3-sentence status summary covering the project state, the open actions, and the gaps.
5. Combine the action-item list, the flagged gaps, and the summary into one final answer.
6. Save that final answer to a file using save_output.

{TOOL_DESCRIPTIONS}

Work step by step. Each reply must contain exactly one ACTION: or one DONE: line.
Do not skip steps. Do not guess file contents — use read_notes() first.
"""

REMINDER = (
    "\n[SYSTEM] Your reply did not contain an ACTION: or DONE: directive. "
    "Please reply with either:\n"
    "  ACTION: tool_name(argument)\n"
    "or:\n"
    "  DONE: <your final answer>\n"
)


# ── Reply parser ──────────────────────────────────────────────────────────────

def parse_reply(reply: str):
    """
    Return ('action', tool_name, arg_text) or ('done', None, answer) or (None, None, None).
    Forgiving: case-insensitive, strips markdown fences, tolerates preamble.
    """
    # Strip markdown code fences
    cleaned = re.sub(r"```[^\n]*\n?(.*?)```", r"\1", reply, flags=re.DOTALL)

    # Search for ACTION: anywhere in the reply (case-insensitive)
    action_match = re.search(
        r"action\s*:\s*(\w+)\s*\(([^)]*)\)",
        cleaned,
        re.IGNORECASE,
    )
    if action_match:
        tool_name = action_match.group(1).strip()
        arg_text = action_match.group(2).strip()
        return ("action", tool_name, arg_text)

    # Search for DONE: anywhere in the reply (case-insensitive)
    done_match = re.search(r"done\s*:\s*(.+)", cleaned, re.IGNORECASE | re.DOTALL)
    if done_match:
        answer = done_match.group(1).strip()
        return ("done", None, answer)

    return (None, None, None)


# ── Agent loop ────────────────────────────────────────────────────────────────

MAX_TURNS = 8

conversation = [{"role": "system", "content": SYSTEM_PROMPT}]
conversation.append({"role": "user", "content": "Please begin."})

final_answer = None
turns_used = 0

for turn in range(MAX_TURNS):
    turns_used += 1

    reply = chat(conversation)
    conversation.append({"role": "assistant", "content": reply})

    kind, name, value = parse_reply(reply)

    if kind == "action":
        fn = TOOLS.get(name)
        if fn is None:
            result = f"[ERROR] Unknown tool: {name}"
        else:
            try:
                result = fn(value) if value else fn()
            except Exception as e:
                result = f"[ERROR] {e}"
        tool_msg = f"[Tool result for {name}]: {result}"
        conversation.append({"role": "user", "content": tool_msg})

    elif kind == "done":
        final_answer = value
        break

    else:
        # Neither keyword found — send a reminder and count the turn
        conversation.append({"role": "user", "content": REMINDER})


# ── Output ────────────────────────────────────────────────────────────────────

print("=" * 60)
print("FINAL ANSWER:")
print("=" * 60)
if final_answer:
    print(final_answer)
else:
    print("[Agent did not produce a DONE reply within the turn limit.]")

print(f"\nTurns used: {turns_used}")
print(f"\nSTATS: {STATS}")
