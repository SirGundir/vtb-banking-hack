include .env

generate-api:
	bunx openapi-generator-cli generate \
		-i ${VITE_SWAGGER_URL} \
		-g typescript-fetch \
		-o ${VITE_API_OUTPUT_PATH}