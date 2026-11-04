#!/usr/bin/env python3
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Renders the catalogue table in README.md from every template.yaml.

  catalogue.py          rewrite README.md between the catalogue markers
  catalogue.py --check  fail if README.md is out of date (CI)

Badges come straight from `supports`, so they cannot drift from the templates.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
START, END = "<!-- catalogue:start -->", "<!-- catalogue:end -->"
BADGES = [("ingress", "🌐"), ("monitoring", "📈"), ("statusPage", "📊"), ("dashboard", "🏠"),
          ("swarm", "🐝"), ("backup", "💾"), ("sso", "🔑"), ("arm64", "🦾")]


def field(text, name):
    m = re.search(rf"^  {name}:\s*(.+?)\s*$", text, re.M)
    return m.group(1).strip().strip('"') if m else ""


def supports(text):
    m = re.search(r"^  supports:\s*\{(.*)\}\s*$", text, re.M)
    flags = {}
    if m:
        for part in m.group(1).split(","):
            if ":" in part:
                k, v = part.split(":", 1)
                flags[k.strip()] = v.strip() == "true"
    return flags


def table():
    rows = ["| Template | Project | Tier | Integrations |", "|---|---|---|---|"]
    for tier in ("system", "apps"):
        for path in sorted((ROOT / tier).glob("*/template.yaml")):
            text = path.read_text()
            name = path.parent.name
            title, home, source = field(text, "title"), field(text, "homepage"), field(text, "source")
            project = f"[{title}]({home})" if home else title
            if source and source != home and "nepfleet-templates" not in source:
                project += f" · [source]({source})"
            flags = supports(text)
            badges = " ".join(icon for key, icon in BADGES if flags.get(key))
            rows.append(f"| [{name}]({tier}/{name}) | {project} | {field(text, 'tier')} | {badges} |")
    legend = "Legend: " + " · ".join(f"{icon} {key}" for key, icon in BADGES)
    return "\n".join([START, "", legend, "", *rows, "", END])


def main():
    readme = ROOT / "README.md"
    text = readme.read_text()
    if START not in text:
        raise SystemExit("README.md has no catalogue markers")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: table(), text, flags=re.S)
    if "--check" in sys.argv:
        if new != text:
            raise SystemExit("README.md catalogue is out of date: run scripts/catalogue.py")
        return
    readme.write_text(new)


if __name__ == "__main__":
    main()
