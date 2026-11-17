---
name: show-progress
description: "Show progress on a project checklist (default: Catalyst's database split) as a table: each major phase with done, open and percent complete, the overall percentage, and what is still open. Use for /show-progress, 'how far along are we', 'show the migration progress', or 'percentage complete'."
user-invocable: true
argument-hint: "[section name, default 'Database split']"
---

# Show progress

Report how far a checklist in a project's `.ai/todo.md` has got, phase by phase. Read-only: change no file, tick nothing.

## Steps

1. Work from the project root (Catalyst: `~/Projects/catalyst`). The section is the argument, matched case-insensitively
   against the todo's top-level `# ` headings; with no argument it is `Database split`. If it matches nothing, run
   `python3 ~/.ai/skills/show-progress/breakdown.py --list-sections` and ask which one.
2. Get the numbers from the script, never by counting by hand:

   ```bash
   python3 ~/.ai/skills/show-progress/breakdown.py --section "<section>"
   ```

   Each `## ` heading in the section is a phase. Only top-level checklist items count: `- [x]` done, `- [ ]` and
   `- [?]` open. Nested bullets are notes. An open item marked `**Later**`, and every item in a phase whose heading
   says `(optional)`, is shown but left out of the required totals, so the overall figure tracks planned work.
3. Present the script's table as is. The table is the answer.
4. Under it, add only what the counts cannot show, in a few short lines:
   - **Effort:** if the open items are much larger or smaller than the done ones (one migration-heavy phase left,
     say), say so and give a rough effort-weighted figure, labelled as an estimate.
   - **In flight:** items with work done but not ticked (a note says "Built", "Step 1 done", a session's commit is
     unpushed, or something is not yet applied to lab). Check the item's nested notes in the todo for this.
   - **Blocked:** open items waiting on the owner (a go-ahead, a credential, a decision) rather than on work.
   - **Next:** the open items whose prerequisites are met, as a short list. Do not start them.
5. Keep it short. Do not repeat each item's history; the todo has it.

## Notes

- The script's item summary is the item's first sentence, cut to about 110 characters. Read the todo when one is
  unclear.
- A phase counts as complete only when every required item is ticked. Do not round a phase up because its last item
  is "nearly done".
