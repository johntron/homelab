ANSIBLE_PLAYBOOK ?= ansible-playbook
ANSIBLE_LINT ?= ansible-lint
YAMLLINT ?= yamllint

.PHONY: lint syntax-check check inspect

lint:
	$(YAMLLINT) .
	$(ANSIBLE_LINT)

syntax-check:
	$(ANSIBLE_PLAYBOOK) --syntax-check playbooks/inspect.yml

check:
	$(ANSIBLE_PLAYBOOK) -i inventory/hosts.yml playbooks/site.yml --check --diff

inspect:
	$(ANSIBLE_PLAYBOOK) -i inventory/hosts.yml playbooks/inspect.yml
