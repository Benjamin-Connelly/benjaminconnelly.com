.PHONY: build clean push serve dev watch open

INFRA_DIR ?= ../benjaminconnelly-infra
ANSIBLE_DIR := $(INFRA_DIR)/ansible
DEV_PORT ?= 8000

build:
	python3 site/build.py

push: build
	bd sync
	ANSIBLE_CONFIG=$(abspath $(INFRA_DIR)/ansible.cfg) \
	ansible-playbook -i $(ANSIBLE_DIR)/inventory/cloud.yml \
		-e @$(ANSIBLE_DIR)/group_vars/all.yml \
		-e "site_output_dir=$(CURDIR)/site/output/" \
		$(ANSIBLE_DIR)/playbooks/push-content.yml

serve: build
	@echo "  Serving at http://localhost:$(DEV_PORT)"
	python3 -m http.server $(DEV_PORT) -d site/output

dev: serve

watch: build
	@echo "  Serving at http://localhost:$(DEV_PORT) (watching for changes)"
	@python3 -m http.server $(DEV_PORT) -d site/output &
	@while true; do \
		find site/content site/templates site/static -type f | entr -d make build; \
	done

open: build
	@python3 -m http.server $(DEV_PORT) -d site/output &
	@sleep 0.5
	@xdg-open http://localhost:$(DEV_PORT) 2>/dev/null || open http://localhost:$(DEV_PORT) 2>/dev/null
	@echo "  Opened http://localhost:$(DEV_PORT) — press Ctrl+C to stop"
	@wait

clean:
	rm -rf site/output/
