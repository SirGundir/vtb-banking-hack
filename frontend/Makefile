include .env

generate-api:
	bunx openapi-generator-cli generate \
		-i ${VITE_SWAGGER_URL} \
		-g typescript-fetch \
		-o ${VITE_API_OUTPUT_PATH}

# Docker команды
docker-up:
	@docker compose -f docker/docker-compose.yml up -d

docker-down:
	@docker compose -f docker/docker-compose.yml down

docker-logs:
	@docker compose -f docker/docker-compose.yml logs -f

docker-restart:
	@docker compose -f docker/docker-compose.yml restart

docker-rebuild:
	@docker compose -f docker/docker-compose.yml build --no-cache
	@docker compose -f docker/docker-compose.yml up -d

docker-build:
	@docker build -f docker/Dockerfile -t vtb-banking-hack-frontend .

docker-run:
	@docker run -d \
		--name vtb-banking-hack-frontend \
		-p 80:80 \
		-e NODE_ENV=production \
		vtb-banking-hack-frontend

docker-stop:
	@docker stop vtb-banking-hack-frontend || true
	@docker rm vtb-banking-hack-frontend || true