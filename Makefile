# Check make version.
MAKE_MIN_VERSION := 3.82
MAKE_OK := $(filter $(MAKE_MIN_VERSION),$(firstword $(sort $(MAKE_VERSION) $(MAKE_MIN_VERSION))))
ifeq ($(MAKE_OK),)
	$(error Make version required $(MAKE_MIN_VERSION)+, current version: $(MAKE_VERSION))
endif

# Versions.
POETRY_VERSION = 1.7.1
PYTHON = python3.10
PIP_VERSION = 22.3.1
SETUPTOOLS_VERSION = 65.6.3
WHEEL_VERSION = 0.38.4

# Paths.
PROJECT_PATH = $(CURDIR)

export VIRTUAL_ENV ?= $(PROJECT_PATH)/.venv_at_$(PYTHON)
VIRTUAL_ENV_POETRY = $(PROJECT_PATH)/.venv_poetry

# Bin.
VENV_ACTIVATE = $(VIRTUAL_ENV)/bin/activate
VENV_POETRY_ACTIVATE = $(VIRTUAL_ENV_POETRY)/bin/activate

# Other.
SHELL = /bin/bash  # Using bash as default shell
CHECK_PYTHON = $(shell which $(PYTHON))

export PATH := $(VIRTUAL_ENV)/bin:$(PATH)
export PYTHONPATH = $(PROJECT_PATH)/menu_planner

all: help

## ------------------------------------------------ SETUP --------------------------------------------------------------

$(VENV_ACTIVATE):
	# Check if correct python is installed.
ifeq ($(CHECK_PYTHON), )
	$(error $(PYTHON) was not found but needed to continue. Please install $(PYTHON))
endif
	$(PYTHON) -m venv $(VIRTUAL_ENV)
	pip install pip==$(PIP_VERSION) setuptools==$(SETUPTOOLS_VERSION) wheel==$(WHEEL_VERSION)

$(VENV_POETRY_ACTIVATE):
	$(PYTHON) -m venv $(VIRTUAL_ENV_POETRY)
	$(VIRTUAL_ENV_POETRY)/bin/pip install pip==$(PIP_VERSION) setuptools==$(SETUPTOOLS_VERSION) wheel==$(WHEEL_VERSION)

# @Setup Install poetry.
poetry: $(VENV_POETRY_ACTIVATE)
	$(VIRTUAL_ENV_POETRY)/bin/pip install poetry==$(POETRY_VERSION)
	ln -f -s $(realpath $(VIRTUAL_ENV_POETRY))/bin/poetry $(VIRTUAL_ENV)/bin/poetry

## @Setup Prepare environment for develop autotests.
install: $(VENV_ACTIVATE) poetry
	# Check user uid
ifeq ($(UID),0)
	$(error Can not run this command as root user)
endif

	poetry install --no-root

## ------------------------------------------------ APP ----------------------------------------------------------------

## @App Start environment.
start: stop
	rm -rf $(PROJECT_PATH)/docker/app_logs && mkdir -p $(PROJECT_PATH)/docker/app_logs
	cd $(PROJECT_PATH)/docker        && \
		docker-compose build --pull  && \
		docker-compose up
stop:
	cd $(PROJECT_PATH)/docker && \
		docker-compose kill   && \
		docker-compose down --volumes

in:
	docker exec -it menu-planner-app bash

reload:
	cd docker && docker-compose restart app


## ------------------------------------------------ TESTS --------------------------------------------------------------

## @Tests Run linters.
lint: $(VENV_ACTIVATE)
	black --check --diff --color $(PROJECT_PATH)/menu_planner
	pylint $(PROJECT_PATH)/menu_planner/

## @Tests Run code formatter.
style: $(VENV_ACTIVATE)
	black $(PROJECT_PATH)/menu_planner

## @Tests Run unittests.
test: $(VENV_ACTIVATE)
	pytest tests

HELP_TARGET_MAX_CHAR_NUM = 20

.PHONY:
help:
	@echo Usage:
	@echo '  make <target>'
	@echo '  make <target> <VAR>=<value>'
	@echo ''
	@awk '/^[a-zA-Z\-\_0-9\/]+:/ \
		{ \
			helpMessage = match(lastLine, /^## (.*)/); \
			if (helpMessage) { \
				helpCommand = substr($$1, 0, index($$1, ":")-1); \
				helpMessage = substr(lastLine, RSTART + 3, RLENGTH); \
				helpGroup = match(helpMessage, /^@([^ ]*)/); \
				if (helpGroup) { \
					helpGroup = substr(helpMessage, RSTART + 1, index(helpMessage, " ")-2); \
					helpMessage = substr(helpMessage, index(helpMessage, " ")+1); \
				} \
				printf "%s|  %-$(HELP_TARGET_MAX_CHAR_NUM)s %s\n", \
					helpGroup, helpCommand, helpMessage; \
			} \
		} \
		{ lastLine = $$0 }' \
		$(MAKEFILE_LIST) \
	| sort -t'|' -sk1,1 -k2,2 \
	| awk -F '|' ' \
			{ \
			cat = $$1; \
			if (cat != lastCat || lastCat == "") { \
				if ( cat == "0" ) { \
					print "Targets: " \
				} else { \
					gsub("_", " ", cat); \
					printf "\nTargets %s:\n", cat; \
				} \
			} \
			print $$2 \
		} \
		{ lastCat = $$1 }'
