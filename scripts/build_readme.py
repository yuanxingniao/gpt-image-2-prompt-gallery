#!/usr/bin/env python3
import json
import html
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "prompts.jsonl"
README = ROOT / "README.md"


def load_records():
    return [json.loads(line) for line in DATA.read_text(encoding="utf-8").splitlines() if line.strip()]


def clean_title(title):
    title = " ".join(str(title).split())
    return title.replace("|", "\\|")


def clean_alt(title):
    return " ".join(str(title).split()).replace('"', "&quot;")


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
        title = clean_title(record["title"])
        alt = clean_alt(record["title"])
        prompt = html.escape(record["prompt"].strip())
        source_url = record["source_url"]
        image = record["image"]

        lines.append(f"### {title}")
        lines.append("")
        lines.append("<table>")
        lines.append("  <tr>")
        lines.append("    <td width=\"38%\" valign=\"top\">")
        lines.append(f"      <img src=\"{image}\" width=\"360\" alt=\"{alt}\">")
        lines.append("    </td>")
        lines.append("    <td width=\"62%\" valign=\"top\">")
        lines.append("      <strong>Prompt</strong>")
        lines.append(f"      <pre>{prompt}</pre>")
        lines.append(f"      <a href=\"{source_url}\">Original post</a>")
        lines.append("    </td>")
        lines.append("  </tr>")
        lines.append("</table>")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    README.write_text(render(load_records()), encoding="utf-8")


if __name__ == "__main__":
    main()
