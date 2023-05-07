local/shell:
	poetry shell

local/install:
	poetry install

local/test:
	pytest .

docker/up:
	docker-compose up -d

docker/down:
	docker-compose down --remove-orphans