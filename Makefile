.PHONY: init lint format test ci

init:
	pip install -e " .[dev]"
	pre-commit install || true

lint:
	ruff check src tests

format:
	black src tests

test:
	pytest

ci: lint format test



