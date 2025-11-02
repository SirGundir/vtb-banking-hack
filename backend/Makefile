down_be:
	@docker compose --profile backend --profile data_loader -f dev-docker-compose.yml down

up_be:
	@docker compose --profile backend --profile data_loader -f dev-docker-compose.yml up

up_d_be:
	@docker compose --profile backend --profile data_loader -f dev-docker-compose.yml up -d

build_be:
	@docker compose --profile backend --profile data_loader -f dev-docker-compose.yml build

user_api_sh:
	@docker compose -f dev-docker-compose.yml exec user_api bash

makemigrations:
ifdef MSG
	@docker compose -f dev-docker-compose.yml exec user_api python -m alembic revision --autogenerate -m "$(MSG)"
else
	@echo "Please provide a migration description: make makemigration MSG='your description'"
endif

db_check:
	@docker compose -f dev-docker-compose.yml exec user_api python -m alembic check

db_head:
	@docker compose -f dev-docker-compose.yml exec user_api python -m alembic upgrade head

user_api_docs:
	@docker compose -f dev-docker-compose.yml exec user_api python main.py dump_docs