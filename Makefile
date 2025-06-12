.PHONY: lint, start, compose-up

lint:
	@echo "Running linters..."
	ruff check --fix .
	ruff format .
	mypy .
	@echo "Linters completed successfully."

start:
	python3 src/main.py

compose-up:
	@echo "Starting Docker containers..."
	cd docker/local && \
		docker compose up --build -d
	@echo "Docker containers started."