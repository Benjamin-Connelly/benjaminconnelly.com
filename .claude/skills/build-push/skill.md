# Build & Push — benjaminconnelly.com

## Trigger phrases
`build`, `push`, `deploy`, `publish site`, `go live`, `make dev`, `preview`, `dev server`, `watch`

## Workflow

### 1. Pre-flight checks

Run ALL checks before proceeding. Report results as a checklist. Any GROUNDED item halts the deploy.

```
[ ] Python deps      — `python3 -c "import markdown, jinja2"` succeeds
[ ] Content exists   — site/content/ has at least one .md file
[ ] Templates exist  — site/templates/ has at least one .j2 file
[ ] Build succeeds   — `make build` exits 0, site/output/ is non-empty
[ ] Infra repo       — ../benjaminconnelly-infra/ exists and has ansible/playbooks/push-content.yml
[ ] SSH key          — ~/.ssh/bconnelly_ryuk exists and has correct permissions (600)
[ ] SSH reachable    — `ssh -o ConnectTimeout=5 -o BatchMode=yes ubuntu@52.43.114.69 true` succeeds
[ ] Ansible installed — `ansible-playbook --version` succeeds
[ ] Git clean        — no uncommitted changes in working tree (warn, don't ground)
```

**On failure, print a clear diagnosis:**

| Check | Failure message |
|---|---|
| Python deps | `GROUNDED: Missing Python packages. Run: pip install -r site/requirements.txt` |
| Content exists | `GROUNDED: No markdown files found in site/content/` |
| Templates exist | `GROUNDED: No Jinja2 templates found in site/templates/` |
| Build fails | `GROUNDED: Build failed. Review build.py output above for errors.` |
| Infra repo | `GROUNDED: Infra repo not found at ../benjaminconnelly-infra/. Clone it or set INFRA_DIR.` |
| SSH key | `GROUNDED: SSH key ~/.ssh/bconnelly_ryuk missing or wrong perms. Run: chmod 600 ~/.ssh/bconnelly_ryuk` |
| SSH unreachable | `GROUNDED: Cannot reach 52.43.114.69. Check VPN, security groups, or instance state.` |
| Ansible missing | `GROUNDED: Ansible not installed. Run: pip install ansible` |
| Git dirty | `WARNING: Uncommitted changes. Consider committing before deploy.` |

### 2. Preview (if not already previewed)

Ask: "Want to preview locally before pushing?"

- If yes: `make dev` (build + serve at http://localhost:8000)
- For live-reload workflow: `make watch` (auto-rebuilds on content/template/static changes)
- To also open browser: `make open`
- If no or already previewed: proceed

### 3. Deploy

```bash
make push
```

This runs:
1. `python3 site/build.py` — generates HTML to site/output/
2. `bd sync` — syncs beads state
3. Ansible `push-content.yml` — rsyncs output/ to /var/www/benjaminconnelly.com on EC2, sets ownership to www-data, reloads nginx

### 4. Post-deploy verification

```bash
curl -s -o /dev/null -w "%{http_code}" https://benjaminconnelly.com
```

Report the HTTP status. 200 = success. Anything else = investigate.

## Quick reference

| Command | What it does |
|---|---|
| `make build` | Build site to site/output/ |
| `make dev` | Build + serve at :8000 |
| `make watch` | Build + serve + auto-rebuild on file changes |
| `make open` | Build + serve + open browser |
| `make push` | Build + deploy to production |
| `make clean` | Wipe site/output/ |
