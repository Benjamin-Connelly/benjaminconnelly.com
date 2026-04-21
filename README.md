# benjaminconnelly.com

Personal and business website. Static site built from Python, deployed to an AWS EC2 host via Ansible playbooks defined in the sibling `infra` repo.

## Architecture

```
content (Markdown + templates)      site/build.py       site/output/
        │                                 │                  │
        └──────── python3 build.py ───────┘                  │
                                                             │
                                                             ▼
                                                  ansible-playbook push-content.yml
                                                             │
                                                             ▼
                                                    EC2 (nginx, Cloudflare DNS)
```

- **Build:** `site/build.py` renders Markdown + Jinja templates into `site/output/`.
- **Deploy:** `ansible/playbooks/push-content.yml` (in the infra repo) syncs `site/output/` to the EC2 host and reloads nginx. No provisioning is done from this repo — the EC2 instance, DNS, and nginx config are all owned by `infra`.
- **Tests:** Playwright smoke tests live in `tests/`. `package.json` exists only for dev tooling; the production deploy is Python-only.

## Quickstart

```bash
make build        # Render the site into site/output/
make serve        # Build and serve on http://localhost:8000
make watch        # Build + serve + auto-rebuild on file changes (needs entr)
make test         # Playwright smoke tests
make push         # Build + deploy via sibling infra Ansible playbook
```

`make push` requires the `infra` repo to be checked out at `../infra` (override with `INFRA_DIR=<path>`) and a working Ansible setup (SOPS age key, `~/.ssh/` access to the EC2 instance).

## Prerequisites

- Python 3.11+ with `site/requirements.txt` installed (`pip install -r site/requirements.txt`).
- Node 20+ for Playwright tests: `npm install && npx playwright install`.
- For `make push`: Ansible + SOPS + age, same as the infra repo.

## Layout

```
site/
  build.py           Entry point for the renderer
  content/           Markdown sources
  templates/         Jinja templates
  static/            CSS, images, client JS
  output/            Build output (gitignored)
tests/               Playwright tests
scripts/             Helper scripts (pre-commit hooks, content tooling)
Makefile             Primary command interface
```

## Deploy Dependency

| What | Where |
|---|---|
| EC2 provisioning, DNS, nginx config, TLS | `infra/terraform/stacks/benjaminconnelly-com/` |
| Ansible playbooks that push content | `infra/ansible/playbooks/push-content.yml` |
| SOPS-encrypted secrets (Cloudflare token, htpasswd, SSH) | `infra/ansible/group_vars/all.sops.yml` |

Changes to this repo don't require a terraform apply. Changes that require infrastructure (new paths, new TLS certs, new nginx config) go in the infra repo.
