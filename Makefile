.PHONY: lint, start

lint:
	@echo "Running linters..."
	ruff check --fix .
	ruff format .
	mypy .
	@echo "Linters completed successfully."

start:
	python3 src/main.py