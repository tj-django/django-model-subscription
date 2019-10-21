# Self-Documented Makefile see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

.DEFAULT_GOAL := help

PYTHON 			:= /usr/bin/env python
MANAGE_PY 		:= $(PYTHON) manage.py
PYTHON_PIP  	:= /usr/bin/env pip
PIP_COMPILE 	:= /usr/bin/env pip-compile
PART 			:= patch
PACKAGE_VERSION = $(shell $(PYTHON) setup.py --version)

# Put it first so that "make" without argument is like "make help".
help:
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-32s-\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.PHONY: help

guard-%: ## Checks that env var is set else exits with non 0 mainly used in CI;
	@if [ -z '${${*}}' ]; then echo 'Environment variable $* not set' && exit 1; fi

# --------------------------------------------------------
# ------- Python package (pip) management commands -------
# --------------------------------------------------------

clean-build: ## Clean project build artifacts.
	@echo "Removing build assets..."
	@$(PYTHON) setup.py clean
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info

install: clean-build  ## Install project dependencies.
	@echo "Installing project in dependencies..."
	@poetry install

install-dev: clean-build  ## Install development extra dependencies.
	@echo "Installing development requirements..."
	@poetry install -E "development"

tag-build:
	@git tag v$(PACKAGE_VERSION)

release-to-pypi: increase-version tag-build  ## Release project to pypi
	@poetry build
	@poetry publish


deploy: release-to-pypi
	@git-changelog . >> CHANGELOG.md


# ----------------------------------------------------------
# ---------- Upgrade project version (bumpversion)  --------
# ----------------------------------------------------------
increase-version: clean-build guard-PART  ## Bump the project version (using the $PART env: defaults to 'patch').
	@echo "Increasing project '$(PART)' version..."
	@poetry up
	@poetry version $(PART)

# ----------------------------------------------------------
# --------- Run project Test -------------------------------
# ----------------------------------------------------------
tox: install-test  ## Run tox test
	@tox

clean-test-all: clean-build  ## Clean build and test assets.
	@rm -rf .tox/
	@rm db.*
