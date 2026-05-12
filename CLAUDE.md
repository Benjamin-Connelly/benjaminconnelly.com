# benjaminconnelly.com

Personal website and blog. Custom Python static site generator (Markdown + Jinja2 → HTML), deployed via the sibling `infra` repo's Ansible to EC2 + nginx + Cloudflare.

## Structure

```
site/
  build.py                Static site builder (markdown → jinja2 → html)
  content/                Markdown source (posts, pages)
  templates/              Jinja2 HTML templates
  static/                 CSS, JS, images
  output/                 Generated HTML (gitignored)
  requirements.txt        Python deps (markdown, jinja2)
Makefile                  Build and deploy commands
docs/                     Project documentation
```

## How it works

`build.py` reads Markdown from `content/`, extracts bold-key metadata (`**Key:** Value`), renders through Jinja2 templates, and writes HTML to `output/`. Markdown extensions in use: tables, fenced_code, toc, meta.

## Quick reference

```bash
# Build the site
make build                    # or: python3 site/build.py

# Local development
make dev                      # build + serve at http://localhost:8000
make watch                    # build + serve + auto-rebuild on file changes
make open                     # build + serve + open browser

# Build and deploy to production
make push                     # builds locally, then runs Ansible deploy from ../infra

# Clean generated output
make clean
```

## Conventions

- Content is Markdown with metadata in bold-key format at the top of each file (`**Title:** ...`, `**Date:** ...`).
- Templates use Jinja2; share partials live under `site/templates/_*.html`.
- Deployment is owned by the `infra` repo's Ansible playbook — local `make push` is a convenience wrapper, not a parallel deploy path.
- `output/` is generated and never committed.

## Skills (this repo)

| Trigger phrases | Skill file |
|---|---|
| `build`, `push`, `deploy`, `go live`, `make dev`, `preview`, `watch` | `.claude/skills/build-push/skill.md` |
| `canvas`, `design canvas`, `new visualization`, `generative art`, `particle effect` | `.claude/skills/canvas-designer/skill.md` |

## Dependencies

```bash
pip install -r site/requirements.txt    # markdown, jinja2
```

The `make watch` target requires `entr` (`apt install entr`).

## Gotchas

- `make push` expects `../infra` to exist (configurable via `INFRA_DIR`).
- `make push` invokes Ansible from the infra repo; needs AWS credentials + SSH access to EC2.
- The `output/` directory is wiped on each build.
- Dev server port is configurable: `make dev DEV_PORT=9000`.

<!-- BEGIN FLEET STANZA v:1 -->
## Personal Fleet Context

This repo is one of several personal repos coordinated under `~/src/personal/ops/`.

**Before making cross-repo decisions, read** `~/src/personal/ops/inventory.md` — authoritative topology, ownership, and dependencies.

**Tracker ownership rule (`bd` issues):**
- IaC, provisioning, secrets, runtime deployment, cross-host concerns → `infra/.beads/`
- ADRs, cross-cutting decisions, fleet topology, inventory changes → `ops/.beads/`
- Application features, bugs, per-project concerns → this repo's `.beads/` (if present)

File a concern in the **upstream-most** tracker whose scope it matches. When in doubt, `ops/.beads/`.

**New repos:** Use `~/src/personal/ops/scripts/new-project.sh` so the new repo is auto-registered in `inventory.md` and wired with this stanza from day one.
<!-- END FLEET STANZA -->
