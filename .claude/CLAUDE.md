# benjaminconnelly.com

Personal website and blog. Custom Python static site generator (Markdown + Jinja2 -> HTML).

## Structure

```
site/
  build.py                Static site builder script
  content/                Markdown source files (posts, pages)
  templates/              Jinja2 HTML templates
  static/                 CSS, JS, images
  output/                 Generated HTML (gitignored)
  requirements.txt        Python dependencies (markdown, jinja2)
Makefile                  Build and deploy commands
docs/                     Project documentation
```

## How It Works

`build.py` reads Markdown files from `content/`, extracts bold-key metadata (`**Key:** Value`), renders through Jinja2 templates, and writes HTML to `output/`. Markdown extensions: tables, fenced_code, toc, meta.

## Key Conventions

- Content is Markdown with metadata in bold-key format at the top of each file
- Templates use Jinja2
- Deployment uses Ansible playbooks from the sibling `benjaminconnelly-infra` repo
- `output/` is generated and should not be committed

## Quick Reference

```bash
# Build the site
make build                    # or: python3 site/build.py

# Build and deploy to production
make push                     # builds, then runs Ansible deploy

# Clean generated output
make clean
```

## Dependencies

```bash
pip install -r site/requirements.txt    # markdown, jinja2
```

## Gotchas

- `make push` expects `../benjaminconnelly-infra` to exist (configurable via `INFRA_DIR`)
- `make push` runs Ansible from the infra repo — needs AWS credentials and SSH access to EC2
- The `output/` directory is wiped on each build
- No dev server included — open `output/index.html` directly or use `python3 -m http.server -d site/output`
