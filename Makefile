.PHONY: install run test lint up down

install:
	python -m pip install -e '.[dev]'

run:
	uvicorn app.main:app --reload

test:
	pytest

lint:
	ruff check .

up:
	docker compose up --build

down:
	docker compose down

