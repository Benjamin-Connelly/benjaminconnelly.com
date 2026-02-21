.PHONY: all sync build deploy clean

SPONGE_DIR := /home/bconnelly/src/personal/sponge/sponge-stamps

all: sync build

sync:
	@echo "Content is authored directly in site/content/ -- no external sync needed"

build:
	python3 site/build.py

deploy:
	ansible-playbook -i ansible/inventory/hosts.yml ansible/playbook.yml

clean:
	rm -rf site/output/
