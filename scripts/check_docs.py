#!/usr/bin/env python3
"""Check local Markdown links in ~/.ai and optional project overlays.

Uses only the standard library. Checks simple inline Markdown links, not
arbitrary Markdown or HTML. Does not validate remote URLs, heading fragments,
or application source claims.

    python3 ~/.ai/scripts/check_docs.py
    python3 ~/.ai/scripts/check_docs.py ~/Projects/catalyst
"""

from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def resolve(doc, target):
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc or not parsed.path:
        return None
    raw = unquote(parsed.path)
    if raw.startswith("~/"):
        return (Path.home() / raw[2:]).resolve()
    if raw.startswith("/"):
        return Path(raw).resolve()
    return (doc.parent / raw).resolve()


def markdown_files(root):
    return sorted(path for path in root.rglob("*.md") if ".git" not in path.parts)


def project_docs(root):
    names = ["AGENTS.md", "CLAUDE.md", "GROK.md", "README.md"]
    docs = [root / name for name in names]
    overlay = root / "ai-engineering-standards"
    if overlay.is_dir():
        docs.extend(markdown_files(overlay))
    index = root / "docs" / "README.md"
    if index.is_file():
        docs.append(index)
    return docs


def main(argv):
    home_guide = Path.home() / ".ai"
    if not home_guide.is_dir():
        print(f"Missing shared guide: {home_guide}")
        return 1

    projects = []
    for arg in argv:
        root = Path(arg).expanduser().resolve()
        if not root.is_dir():
            print(f"Missing project: {root}")
            return 1
        projects.append(root)

    docs = markdown_files(home_guide)
    for root in projects:
        docs.extend(project_docs(root))

    errors = []
    questions = []
    links = 0
    referenced = set()
    seen = set()

    for doc in docs:
        if doc in seen:
            continue
        seen.add(doc)
        if not doc.is_file():
            errors.append(f"Missing document: {doc}")
            continue
        content = doc.read_text(encoding="utf-8")
        prose = re.sub(
            r"^```[^\n]*\n.*?^```[^\n]*$",
            "",
            content,
            flags=re.MULTILINE | re.DOTALL,
        )
        for target in re.findall(r"\[[^\]\n]+\]\(([^)\s]+)\)", prose):
            path = resolve(doc, target)
            if path is None:
                continue
            links += 1
            if not path.exists():
                errors.append(f"{doc}: missing link target {target}")
            else:
                referenced.add(path)
        for number, line in enumerate(content.splitlines(), 1):
            if line == "## todo human":
                questions.append(f"{doc}:{number}")

    for root in projects:
        agents = root / "AGENTS.md"
        if agents.is_file() and "](ai-engineering-standards/README.md)" not in agents.read_text(encoding="utf-8"):
            errors.append(f"{agents.name}: missing link to ai-engineering-standards/README.md")
        for name in ("CLAUDE.md", "GROK.md"):
            entry = root / name
            if entry.is_file() and "](AGENTS.md)" not in entry.read_text(encoding="utf-8"):
                errors.append(f"{name}: missing link to AGENTS.md")
        overlay_index = root / "ai-engineering-standards" / "README.md"
        if overlay_index.is_file() and "](~/.ai/README.md)" not in overlay_index.read_text(encoding="utf-8"):
            errors.append("ai-engineering-standards/README.md: missing link to ~/.ai/README.md")

    home_index = (home_guide / "README.md").resolve()
    warnings = []
    for doc in markdown_files(home_guide):
        if doc.resolve() == home_index:
            continue
        if doc.resolve() not in referenced:
            warnings.append(f"{doc}: not referenced from any checked doc")
    for root in projects:
        overlay = root / "ai-engineering-standards"
        if not overlay.is_dir():
            continue
        project_index = (overlay / "README.md").resolve()
        for doc in markdown_files(overlay):
            if doc.resolve() == project_index:
                continue
            if doc.resolve() not in referenced:
                warnings.append(f"{doc}: not referenced from any checked doc")

    label = home_guide.as_posix()
    if projects:
        label += " + " + ", ".join(root.as_posix() for root in projects)
    if errors:
        print("Documentation check failed:")
        for error in errors:
            print(f"- {error}")
    else:
        print(f"PASS: {len(seen)} documents, {links} local file links ({label}).")
    if warnings:
        print(f"Orphan documents ({len(warnings)}):")
        for warning in warnings:
            print(f"- {warning}")
    print(f"Open human decisions: {len(questions)}")
    for question in questions:
        print(f"- {question}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
