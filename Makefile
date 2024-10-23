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
	tox -e py39-docs

.PHONY: lint
lint:  ## Lint files
	tox exec -e py39-format-check -- black --target-version=py39 --exclude=_vendor setup.py bleach/ tests/ tests_website/
	tox -e py39-lint
	tox -e py39-format-check

.PHONY: vendorverify
vendorverify:  ## Verify vendored files
	tox -e py39-vendorverify

.PHONY: clean
clean:  ## Clean build artifacts
	rm -rf build dist ${PROJECT}.egg-info .tox .pytest_cache
	rm -rf docs/_build/*
	rm -rf .eggs
	find . -name __pycache__ | xargs rm -rf
	find . -name '*.pyc' | xargs rm -rf
