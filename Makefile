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
	poetry run black scripts
	poetry run isort scripts
	poetry run flake8 scripts

format-check:
	@$(info $(DT_NOW) | INFO | Makefile → Linting checking...)
	poetry run black --check scripts
	poetry run isort --check scripts
	poetry run flake8 scripts

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
