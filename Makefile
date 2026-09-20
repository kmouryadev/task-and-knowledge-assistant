.PHONY: install lint typecheck test up down

install:
	pip install -r backend/requirements.txt -r backend/requirements-dev.txt

lint:
	ruff check backend/app backend/tests

typecheck:
	mypy backend/app

test:
	pytest backend/tests -v

up:
	docker compose up --build

down:
	docker compose down
