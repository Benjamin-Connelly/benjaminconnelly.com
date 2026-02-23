#!/usr/bin/env python3
"""Static site builder. Converts markdown content to HTML via Jinja2 templates."""

import os
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

MD_EXTENSIONS = ["tables", "fenced_code", "toc", "meta"]


def extract_metadata(text):
    """Extract bold-key metadata from the top of a markdown document.

    Looks for lines like: **Key:** Value
    Returns (metadata_dict, remaining_text).
    """
    metadata = {}
    lines = text.split("\n")
    content_start = 0

    for i, line in enumerate(lines):
        match = re.match(r"^\*\*(.+?):\*\*\s*(.+)$", line.strip())
        if match:
            metadata[match.group(1).strip()] = match.group(2).strip()
            content_start = i + 1
        elif line.strip() == "":
            content_start = i + 1
        else:
            break

    remaining = "\n".join(lines[content_start:])
    return metadata, remaining


def extract_title(text):
    """Pull the first H1 from markdown text."""
    for line in text.split("\n"):
        if line.startswith("# "):
            return line.lstrip("# ").strip()
    return "Untitled"


def select_template(rel_path):
    """Choose the right template based on content path."""
    rel_str = str(rel_path)

    if rel_str == "index.md":
        return "home.html.j2"
    if rel_str == "research/index.md":
        return "index.html.j2"
    return "doc.html.j2"


def build_output_path(rel_path):
    """Convert a content .md path to an output .html path."""
    return rel_path.with_suffix(".html")


def build():
    """Build the site."""
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True)

    # Copy static assets
    if STATIC_DIR.exists():
        for item in STATIC_DIR.iterdir():
            dest = OUTPUT_DIR / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)
        print(f"  Copied static assets to {OUTPUT_DIR}")

    # Set up Jinja2
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))
    md = markdown.Markdown(extensions=MD_EXTENSIONS)

    # Process all markdown files (skip index.md — homepage is mirrorball.html)
    md_files = sorted(CONTENT_DIR.rglob("*.md"))

    for md_file in md_files:
        if md_file.relative_to(CONTENT_DIR) == Path("index.md"):
            continue
        rel_path = md_file.relative_to(CONTENT_DIR)
        out_path = OUTPUT_DIR / build_output_path(rel_path)

        print(f"  Building {rel_path} -> {out_path.relative_to(OUTPUT_DIR)}")

        raw_text = md_file.read_text(encoding="utf-8")

        metadata, content_text = extract_metadata(raw_text)
        title = extract_title(raw_text)

        md.reset()
        html_content = md.convert(content_text)

        template_name = select_template(rel_path)
        template = env.get_template(template_name)

        rendered = template.render(
            content=html_content,
            title=title,
            metadata=metadata if metadata else None,
        )

        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8")

    # Use mirrorball as the homepage
    mirrorball_src = OUTPUT_DIR / "mirrorball.html"
    mirrorball_dst = OUTPUT_DIR / "index.html"
    if mirrorball_src.exists():
        shutil.copy2(mirrorball_src, mirrorball_dst)
        mirrorball_src.unlink()
        print("  Installed mirrorball.html as index.html")

    print(f"\n  Built {len(md_files)} pages to {OUTPUT_DIR}")


if __name__ == "__main__":
    print("Building site...")
    build()
    print("Done.")
