# Self-Documented Makefile see https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html

.DEFAULT_GOAL := help

PYTHON 			:= /usr/bin/env python
MANAGE_PY 		:= $(PYTHON) manage.py
PYTHON_PIP  	:= /usr/bin/env pip
PIP_COMPILE 	:= /usr/bin/env pip-compile
PART 			:= patch
DOCS_DIR 		:= ./docs
DOC_SOURCE_DIR 	:= source
DOC_BUILD_DIR 	:= build
DOC_SERVE_PORT	:= 8080

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
	@rm -rf build dist *.egg-info

install: clean-build  ## Install project dependencies.
	@echo "Installing project in dependencies..."
	@pip install -U pip setuptools poetry
ifeq "$(shell uname)" "Darwin"
	@export LDFLAGS="-L/usr/local/opt/openssl/lib"
	@export CPPFLAGS="-I/usr/local/opt/openssl/include"
endif
	@pip install poetry==1.1.4
	@poetry install -vvv
	@poetry update

install-dev: clean-build install  ## Install development extra dependencies.
	@echo "Installing development requirements..."
	@poetry install -E "development"

tag-build:
	@git tag v$(shell cat pyproject.toml | grep -E "^version" | sed 's/["= ]//g;s/version//g')

release-to-pypi: increase-version tag-build  ## Release project to pypi
	@poetry build
	@poetry publish
	@git-changelog . > CHANGELOG.md
	@git commit -am "Synced pyproject.toml and updated CHANGELOG.md."
	@git push --tags
	@git push

# --------------------------------------------------------
# ----- Sphinx Documentation commands --------------------
# --------------------------------------------------------
build-docs:
	@echo "Building docs..."
	@$(MAKE) -C $(DOCS_DIR) SPHINXOPTS='-W' clean html

github:
	@cd $(DOCS_DIR) && make github

view-docs: build-docs  ## Serve sphinx doc locally.
	@echo "Serving documentation..."
	@cd $(DOCS_DIR) && sphinx-autobuild $(DOC_SOURCE_DIR) $(DOC_BUILD_DIR) -p $(DOC_SERVE_PORT)

# ----------------------------------------------------------
# ---------- Upgrade project version (bumpversion)  --------
# ----------------------------------------------------------
increase-version: clean-build guard-PART  ## Bump the project version (using the $PART env: defaults to 'patch').
	@echo "Increasing project '$(PART)' version..."
	@poetry update
	@poetry version $(PART)

# ----------------------------------------------------------
# --------- Run project Test -------------------------------
# ----------------------------------------------------------
tox:  ## Run tox test
	@pip install "tox>=3.14" tox-gh-actions
	@tox

clean-test-all: clean-build  ## Clean build and test assets.
	@rm -rf .tox db.* .mypy_cache

# ----------------------------------------------------------
# ---------- Managment Commands ----------------------------
# ----------------------------------------------------------
test:
	@python manage.py test --no-input
