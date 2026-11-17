#!/usr/bin/env python3
"""Progress breakdown of one section of a project's .ai/todo.md, as a Markdown table.

  python3 breakdown.py [--todo PATH] [--section TEXT] [--list-sections]

The section is a top-level "# " heading; its "## " headings are the phases. Only top-level checklist items count
("- [x]" done, "- [ ]" or "- [?]" open); nested bullets are notes. An item marked **Later** and every item in a phase
whose heading says "(optional)" are shown but left out of the required totals, so the overall percentage tracks the
work that is actually planned. Items before the first "## " belong to a phase named after the section.

Read-only. Exit status: 0 printed; 2 no todo file, no such section, or a section with no checklist items.
"""

import argparse
import re
import sys
from pathlib import Path

ITEM = re.compile(r"^- \[( |x|X|\?)\] (.*)$")
ITEM_ID = re.compile(r"\*\*([A-Z][A-Z0-9]*(?:-[A-Z0-9.]+)+)\*\*")


def sections(lines):
    return [line[2:].strip() for line in lines if line.startswith("# ")]


def pick(lines, wanted):
    """Lines of the first top-level section whose heading contains `wanted` (case-insensitive)."""
    out, inside = [], False
    for line in lines:
        if line.startswith("# "):
            if inside:
                break
            inside = wanted.lower() in line[2:].lower()
            title = line[2:].strip()
            continue
        if inside:
            out.append(line)
    return (title, out) if inside or out else (None, None)


def summary(text):
    """The item's text without its tag words and ID, cut to one short line."""
    text = re.sub(r"\*\*(api|database|security|docs|test|build|ops|infra|code|Later)\*\*\s*", "", text)
    text = ITEM_ID.sub("", text, count=1).strip()
    text = re.sub(r"\s+", " ", text)
    # First sentence; a sentence that only introduces a list ("...:") keeps going into the next one.
    parts = re.split(r"(?<=[.;])\s", text)
    first = parts[0]
    if first.endswith(":") or len(first) < 25:
        first = " ".join(parts[:2])
    return (first[:110].rstrip() + "…") if len(first) > 111 else first


def parse(title, lines):
    phases, current = [], {"name": title, "optional": False, "items": []}
    for line in lines:
        if line.startswith("## "):
            if current["items"] or phases or current["name"] != title:
                phases.append(current)
            name = line[3:].strip()
            current = {"name": name, "optional": "(optional)" in name.lower(), "items": []}
            continue
        m = ITEM.match(line)
        if m:
            body = m.group(2)
            ident = ITEM_ID.search(body)
            current["items"].append({
                "done": m.group(1) in "xX",
                "later": "**Later**" in body,
                "id": ident.group(1) if ident else "",
                "text": summary(body),
            })
    phases.append(current)
    return [p for p in phases if p["items"]]


def pct(done, total):
    return "—" if total == 0 else f"{round(100 * done / total)}%"


def render(title, phases):
    out = [f"## {title}: progress", "",
           "| Phase | Done | Open | Complete |", "|---|---|---|---|"]
    req_done = req_total = 0
    for p in phases:
        counted = [i for i in p["items"] if not p["optional"] and not (i["later"] and not i["done"])]
        done = sum(i["done"] for i in counted)
        total = len(counted)
        later = sum(1 for i in p["items"] if i["later"] and not i["done"])
        if not p["optional"]:
            req_done += done
            req_total += total
        name = p["name"] + (" *(not counted)*" if p["optional"] else "")
        shown_done = sum(i["done"] for i in p["items"]) if p["optional"] else done
        shown_total = len(p["items"]) if p["optional"] else total
        open_n = shown_total - shown_done
        note = f" (+{later} later)" if later and not p["optional"] else ""
        out.append(f"| {name} | {shown_done} of {shown_total}{note} | {open_n} | **{pct(shown_done, shown_total)}** |")
    out.append(f"| **Overall (required)** | **{req_done} of {req_total}** | **{req_total - req_done}** | **{pct(req_done, req_total)}** |")
    out += ["", "### Open items", ""]
    any_open = False
    for p in phases:
        rest = [i for i in p["items"] if not i["done"]]
        if not rest:
            continue
        any_open = True
        out.append(f"**{p['name']}**")
        for i in rest:
            tag = " *(later)*" if i["later"] else ""
            ident = f"{i['id']}: " if i["id"] else ""
            out.append(f"- {ident}{i['text']}{tag}")
        out.append("")
    if not any_open:
        out.append("Nothing open.")
    return "\n".join(out).rstrip() + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--todo", default=".ai/todo.md")
    ap.add_argument("--section", default="Database split")
    ap.add_argument("--list-sections", action="store_true")
    args = ap.parse_args(argv)
    path = Path(args.todo)
    if not path.is_file():
        print(f"error: no todo file at {path}", file=sys.stderr)
        return 2
    lines = path.read_text(encoding="utf-8").splitlines()
    if args.list_sections:
        print("\n".join(sections(lines)))
        return 0
    title, body = pick(lines, args.section)
    if title is None:
        print(f"error: no '# ' section matching {args.section!r}. Sections: {', '.join(sections(lines))}", file=sys.stderr)
        return 2
    phases = parse(title, body)
    if not phases:
        print(f"error: section {title!r} has no checklist items", file=sys.stderr)
        return 2
    sys.stdout.write(render(title, phases))
    return 0


if __name__ == "__main__":
    sys.exit(main())
