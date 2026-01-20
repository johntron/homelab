ANSIBLE_DIR := ansible

.PHONY: lint check apply bootstrap inspect inventory discover summarize ping

lint:
	$(MAKE) -C $(ANSIBLE_DIR) lint

check:
	$(MAKE) -C $(ANSIBLE_DIR) check TAGS="$(TAGS)" LIMIT="$(LIMIT)"

apply:
	$(MAKE) -C $(ANSIBLE_DIR) apply TAGS="$(TAGS)" LIMIT="$(LIMIT)" CONFIRM="$(CONFIRM)"

bootstrap:
	$(MAKE) -C $(ANSIBLE_DIR) bootstrap

inspect:
	$(MAKE) -C $(ANSIBLE_DIR) inspect

inventory:
	$(MAKE) -C $(ANSIBLE_DIR) inventory

discover:
	$(MAKE) -C $(ANSIBLE_DIR) discover LIMIT="$(LIMIT)"

summarize:
	python3 scripts/summarize_discovery.py

ping:
	$(MAKE) -C $(ANSIBLE_DIR) ping LIMIT="$(LIMIT)"
