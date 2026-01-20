ANSIBLE_PLAYBOOK ?= ansible-playbook
ANSIBLE_LINT ?= ansible-lint
YAMLLINT ?= yamllint
INVENTORY ?= inventory/hosts.yml
TAGS ?=
LIMIT ?=
TAGS_ARGS := $(if $(TAGS),--tags $(TAGS),)
LIMIT_ARGS := $(if $(LIMIT),--limit $(LIMIT),)

.PHONY: lint syntax-check check inspect inventory apply bootstrap discover ping

lint:
	$(YAMLLINT) .
	$(ANSIBLE_LINT)

syntax-check:
	$(ANSIBLE_PLAYBOOK) --syntax-check playbooks/inspect.yml

check:
	$(ANSIBLE_PLAYBOOK) -i $(INVENTORY) playbooks/site.yml --check --diff $(TAGS_ARGS) $(LIMIT_ARGS)

inspect:
	$(ANSIBLE_PLAYBOOK) -i $(INVENTORY) playbooks/inspect.yml

inventory:
	ansible-inventory -i $(INVENTORY) --list

apply:
	@if [ "$(CONFIRM)" != "1" ]; then echo "Set CONFIRM=1 to apply changes."; exit 1; fi
	$(ANSIBLE_PLAYBOOK) -i $(INVENTORY) playbooks/site.yml $(TAGS_ARGS) $(LIMIT_ARGS)

bootstrap:
	$(ANSIBLE_PLAYBOOK) -i $(INVENTORY) playbooks/bootstrap.yml $(TAGS_ARGS)

discover:
	$(ANSIBLE_PLAYBOOK) -i $(INVENTORY) playbooks/discover.yml $(LIMIT_ARGS)

ping:
	ansible all -i $(INVENTORY) -m ping $(LIMIT_ARGS)
