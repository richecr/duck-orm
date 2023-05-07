local/shell:
	poetry shell

local/install:
	poetry install

local/test:
	pytest . --cov=duck_orm tests/ --cov-report html

local/build:
	poetry build

docker/up:
	docker-compose up -d

docker/down:
	docker-compose down --remove-orphans