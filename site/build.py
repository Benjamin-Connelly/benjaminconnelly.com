#!/usr/bin/env python3
"""Static site builder. Converts markdown content to HTML via Jinja2 templates."""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import markdown
from jinja2 import Environment, FileSystemLoader

SITE_DIR = Path(__file__).parent
CONTENT_DIR = SITE_DIR / "content"
TEMPLATE_DIR = SITE_DIR / "templates"
STATIC_DIR = SITE_DIR / "static"
OUTPUT_DIR = SITE_DIR / "output"

MD_EXTENSIONS: list[str] = ["tables", "fenced_code", "toc", "meta"]

# Lines like: **Key:** Value
_META_LINE = re.compile(r"^\*\*(.+?):\*\*\s*(.+)$")


def extract_metadata(text: str) -> tuple[dict[str, str], str]:
    """Extract bold-key metadata from the top of a markdown document.

    Scans consecutive `**Key:** Value` lines (with optional blank lines between
    them) from the top. Stops at the first line that is neither blank nor a
    metadata line. Returns (metadata_dict, remaining_body).
    """
    metadata: dict[str, str] = {}
    lines = text.split("\n")
    body_start = 0

    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        match = _META_LINE.match(stripped)
        if not match:
            body_start = i
            break
        metadata[match.group(1).strip()] = match.group(2).strip()
    else:
        # No non-blank, non-metadata line encountered — the whole file is metadata.
        body_start = len(lines)

    return metadata, "\n".join(lines[body_start:])


def extract_title(text: str) -> str:
    """Pull the first H1 from markdown text."""
    for line in text.split("\n"):
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    return "Untitled"


def select_template(rel_path: Path) -> str:
    """Choose the right template based on content path."""
    rel_str = str(rel_path)
    if rel_str == "index.md":
        return "index.html.j2"
    if rel_str == "research/index.md":
        return "research.html.j2"
    return "doc.html.j2"


def build_output_path(rel_path: Path) -> Path:
    """Convert a content .md path to an output .html path."""
    return rel_path.with_suffix(".html")


def build() -> None:
    """Build the site into OUTPUT_DIR."""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    if STATIC_DIR.exists():
        for item in STATIC_DIR.iterdir():
            dest = OUTPUT_DIR / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)
        print(f"  Copied static assets to {OUTPUT_DIR}")

    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    md = markdown.Markdown(extensions=MD_EXTENSIONS)

    # index.html is served directly from static/ (the card gallery landing page),
    # so we skip content/index.md. All other markdown files go through templates.
    md_files = sorted(CONTENT_DIR.rglob("*.md"))

    for md_file in md_files:
        rel_path = md_file.relative_to(CONTENT_DIR)
        if rel_path == Path("index.md"):
            continue
        out_path = OUTPUT_DIR / build_output_path(rel_path)

        print(f"  Building {rel_path} -> {out_path.relative_to(OUTPUT_DIR)}")

        raw_text = md_file.read_text(encoding="utf-8")
        metadata, content_text = extract_metadata(raw_text)
        title = extract_title(raw_text)

        md.reset()
        html_content = md.convert(content_text)

        template = env.get_template(select_template(rel_path))
        rendered = template.render(
            content=html_content,
            title=title,
            metadata=metadata if metadata else None,
        )

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8")

    print(f"\n  Built {len(md_files)} pages to {OUTPUT_DIR}")


if __name__ == "__main__":
    print("Building site...")
    build()
    print("Done.")
