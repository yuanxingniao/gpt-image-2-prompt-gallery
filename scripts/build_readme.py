#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "prompts.jsonl"
README = ROOT / "README.md"


def load_records():
    return [json.loads(line) for line in DATA.read_text(encoding="utf-8").splitlines() if line.strip()]


def render(records):
    lines = []
    lines.append("# GPT Image 2 Prompt Gallery")
    lines.append("")
    lines.append("A curated gallery of GPT-Image-2 prompt examples with one reviewed output image per prompt.")
    lines.append("")
    lines.append("> Source links point to the original public X/Twitter posts. Images are archived locally for stable GitHub display. If you are a rights holder and want a case removed or corrected, please open an issue.")
    lines.append("")
    lines.append(f"**Cases:** {len(records)}")
    lines.append("")
    lines.append("## Cases")
    lines.append("")
    for record in records:
        lines.append(f"### {record['title']}")
        lines.append("")
        lines.append(f"[Original post]({record['source_url']})")
        lines.append("")
        lines.append("| Output |")
        lines.append("| :----: |")
        lines.append(f"| <img src=\"{record['image']}\" width=\"360\" alt=\"{record['title']}\"> |")
        lines.append("")
        lines.append("**Prompt:**")
        lines.append("")
        lines.append("```text")
        lines.append(record["prompt"].strip())
        lines.append("```")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    README.write_text(render(load_records()), encoding="utf-8")


if __name__ == "__main__":
    main()
