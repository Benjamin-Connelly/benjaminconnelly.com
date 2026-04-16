.PHONY: help build clean push serve dev watch open

INFRA_DIR ?= ../benjaminconnelly-infra
ANSIBLE_DIR := $(INFRA_DIR)/ansible
DEV_PORT ?= 8000

help:  ## Show this help
	@awk 'BEGIN { FS = ":.*## "; printf "Targets:\n" } \
	     /^[a-zA-Z_-]+:.*## / { printf "  %-10s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)
	@echo ""
	@echo "Overrides: DEV_PORT=$(DEV_PORT)  INFRA_DIR=$(INFRA_DIR)"

build:  ## Build the static site into site/output/
	python3 site/build.py

push: build  ## Build, sync beads, deploy via Ansible
	bd sync
	ANSIBLE_CONFIG=$(abspath $(INFRA_DIR)/ansible.cfg) \
	ansible-playbook -i $(ANSIBLE_DIR)/inventory/cloud.yml \
		-e @$(ANSIBLE_DIR)/group_vars/all.yml \
		-e "site_output_dir=$(CURDIR)/site/output/" \
		$(ANSIBLE_DIR)/playbooks/push-content.yml

serve: build  ## Build and serve at http://localhost:$(DEV_PORT)
	@echo "  Serving at http://localhost:$(DEV_PORT)"
	python3 -m http.server $(DEV_PORT) -d site/output

dev: serve  ## Alias for serve

watch: build  ## Build + serve + auto-rebuild on file changes (needs entr)
	@echo "  Serving at http://localhost:$(DEV_PORT) (watching for changes)"
	@trap 'kill %1 2>/dev/null' EXIT INT TERM; \
	python3 -m http.server $(DEV_PORT) -d site/output & \
	while true; do \
		find site/content site/templates site/static -type f | entr -d make build; \
	done

open: build  ## Build, serve, and open in default browser
	@trap 'kill %1 2>/dev/null' EXIT INT TERM; \
	python3 -m http.server $(DEV_PORT) -d site/output & \
	sleep 0.5; \
	xdg-open http://localhost:$(DEV_PORT) 2>/dev/null || open http://localhost:$(DEV_PORT) 2>/dev/null; \
	echo "  Opened http://localhost:$(DEV_PORT) — press Ctrl+C to stop"; \
	wait

clean:  ## Remove generated output
	rm -rf site/output/
