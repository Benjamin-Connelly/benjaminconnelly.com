.PHONY: all sync build deploy clean

SPONGE_DIR := /home/bconnelly/src/personal/sponge/sponge-stamps

all: sync build

sync:
	rsync -av --delete $(SPONGE_DIR)/research/ site/content/research/sponge-stamps/
	rsync -av --delete $(SPONGE_DIR)/procurement/ site/content/research/procurement/

build:
	python site/build.py

deploy:
	ansible-playbook -i ansible/inventory/hosts.yml ansible/playbook.yml

clean:
	rm -rf site/output/
