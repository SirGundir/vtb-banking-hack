include backend/Makefile

down_all:
	@docker compose -f dev-docker-compose.yml down

up_all:
	@docker compose -f dev-docker-compose.yml up

up_d_all:
	@docker compose -f dev-docker-compose.yml up -d

build_all:
	@docker compose -f dev-docker-compose.yml build --no-cache

down_dev:
	@docker compose --profile frontend --profile backend -f dev-docker-compose.yml down

up_dev:
	@docker compose --profile frontend --profile backend -f dev-docker-compose.yml up

up_d_dev:
	@docker compose --profile frontend --profile backend -f dev-docker-compose.yml up -d

build_dev:
	@docker compose --profile frontend --profile backend -f dev-docker-compose.yml build

logs_dev:
	@docker compose -f dev-docker-compose.yml logs -f
