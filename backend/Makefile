down:
	@docker compose -f dev-docker-compose.yml down

up:
	@docker compose -f dev-docker-compose.yml up

up_d:
	@docker compose -f dev-docker-compose.yml up -d

build:
	@docker compose -f dev-docker-compose.yml build

user_api_sh:
	@docker compose -f dev-docker-compose.yml exec user_api bash

makemigrations:
ifdef MSG
	@docker compose -f dev-docker-compose.yml exec user_api python -m alembic revision --autogenerate -m "$(MSG)"
else
	@echo "Please provide a migration description: make makemigration MSG='your description'"
endif

check:
	@docker compose -f dev-docker-compose.yml exec user_api python -m alembic check

head:
	@docker compose -f dev-docker-compose.yml exec user_api python -m alembic upgrade head