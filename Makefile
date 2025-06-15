.PHONY: lint, start, compose-up, migrate, revision

lint:
	@echo "Running linters..."
	ruff check --fix .
	ruff format .
	mypy .
	@echo "Linters completed successfully."

start:
	python3 main.py

compose-up:
	@echo "Starting Docker containers..."
	cd docker/local && \
		docker compose up --build -d
	@echo "Docker containers started."

migrate:
	poetry run alembic upgrade head

revision:
	TZ=UTC poetry run alembic revision -m rename-me

autogenerate:
	poetry run alembic revision --autogenerate -m "Auto-generated migration"