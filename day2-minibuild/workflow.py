#!/usr/bin/env python3

import os
from common.llm import chat, STATS

# Get the directory where this scrip11t is located
script_dir = os.path.dirname(os.path.abspath(__file__))
# Construct the path to notes.txt relative to this script
notes_path = os.path.join(script_dir, 'notes.txt')

# Read the notes file
with open(notes_path, 'r') as f:
    notes_content = f.read()

# Step 1: Extract action items
response1 = chat([
    {"role": "system", "content": "Extract every action item from the notes as a list of task / owner / deadline. Use 'MISSING' when an owner or deadline is absent. Ignore ideas that were explicitly parked."},
    {"role": "user", "content": notes_content}
])

# Step 2: Find items with MISSING owner or deadline
response2 = chat([
    {"role": "system", "content": "Given a list of action items (task, owner, deadline), output only the items that have a MISSING owner or deadline."},
    {"role": "user", "content": response1}
])

# Step 3: Write status summary
response3 = chat([
    {"role": "system", "content": "Given the list of action items and flagged items, write a 3-sentence status summary about the project progress."},
    {"role": "user", "content": f"Action Items: {response1}\n\nFlagged Items: {response2}"}
])

# Print results
print("Action Items:")
print(response1)

print("\nFlagged Items (missing owner or deadline):")
print(response2)

print(f"\nStatus Summary:\n{response3}")

print(f"\nSTATS:\n{STATS}")