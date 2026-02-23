.PHONY: build clean push

INFRA_DIR ?= ../benjaminconnelly-infra
ANSIBLE_DIR := $(INFRA_DIR)/ansible

build:
	python3 site/build.py

push: build
	bd sync
	ANSIBLE_CONFIG=$(abspath $(INFRA_DIR)/ansible.cfg) \
	ansible-playbook -i $(ANSIBLE_DIR)/inventory/cloud.yml \
		-e @$(ANSIBLE_DIR)/group_vars/all.yml \
		-e "site_output_dir=$(CURDIR)/site/output/" \
		$(ANSIBLE_DIR)/playbooks/push-content.yml

clean:
	rm -rf site/output/
