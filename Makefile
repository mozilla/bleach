DEFAULT_GOAL := help
PROJECT=bleach

.PHONY: help
help:
	@echo "Available rules:"
	@fgrep -h "##" Makefile | fgrep -v fgrep | sed 's/\(.*\):.*##/\1:  /'

.PHONY: test
test:  ## Run tests
	tox

.PHONY: docs
docs:  ## Build docs
	tox -e py310-docs

.PHONY: format
format:  ## Format Python files
	tox exec -e py310-lint -- ruff format --target-version=py310 --exclude=_vendor setup.py bleach/ tests/ tests_website/

.PHONY: lint
lint:  ## Lint files
	tox -e py310-lint

.PHONY: vendorverify
vendorverify:  ## Verify vendored files
	tox -e py310-vendorverify

.PHONY: clean
clean:  ## Clean build artifacts
	rm -rf build dist ${PROJECT}.egg-info .tox .pytest_cache
	rm -rf docs/_build/*
	rm -rf .eggs
	find . -name __pycache__ | xargs rm -rf
	find . -name '*.pyc' | xargs rm -rf
