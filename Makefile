NOW = $(shell date)

# Project setup
init:
	@$(info $(NOW) | INFO | Makefile → Project setup...)
	poerty install

# Export requirements
requirements:
	@$(info $(NOW) | INFO | Makefile → Export requirements from pyproject.toml file...)
	poetry export --format=requirements.txt --without-hashes --output=requirements.txt

# Linting
lint:
	@$(info $(DT_NOW) | INFO | Makefile → Linting...)
	poetry run black dv2_airflow
	poetry run isort dv2_airflow
	poetry run flake8 dv2_airflow

lint-check:
	@$(info $(DT_NOW) | INFO | Makefile → Linting checking...)
	poetry run black --check dv2_airflow
	poetry run isort --check dv2_airflow
	poetry run flake8 dv2_airflow

# Docker
up:
	@$(info $(NOW) | INFO | Makefile → Docker up...)
	docker-compose up

up-b:
	@$(info $(NOW) | INFO | Makefile → Docker buikld & up...)
	docker-compose up --build

down:
	@$(info $(NOW) | INFO | Makefile → Docker down...)
	docker-compose down

prune-a:
	@$(info $(NOW) | INFO | Makefile → Pruning Docker containers...)
	docker system prune -a
