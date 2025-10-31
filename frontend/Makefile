export SWAGGER_URL=http://localhost:4000/openapi.json
export API_OUTPUT_PATH=./src/api

generate-api:
	bunx openapi-generator-cli generate \
		-i $$SWAGGER_URL \
		-g typescript-fetch \
		-o $$API_OUTPUT_PATH