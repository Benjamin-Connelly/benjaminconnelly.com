# benjaminconnelly.com

Personal and business static site. Built with Python, deployed via the infra repo's Ansible to EC2 + nginx + Cloudflare.

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
