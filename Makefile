docker-build:
	docker buildx build \
	--build-arg BASE_LAYER=base-dev \
	-t llm-gateway .

docker-test:
	docker buildx build \
	--build-arg BASE_LAYER=base-dev \
	--target backend-test-suite \
	-t llm-gateway-test .

	docker run -ti llm-gateway-test pytest $(TEST_OPTIONS)

browse:
	open http://localhost:3000

browse-api:
	open http://localhost:5000/api/docs

up: docker-build
	docker-compose -p llm-gateway -f docker-compose.yml up --detach

down:
	docker-compose -p llm-gateway -f docker-compose.yml down
	docker-compose rm  # force postgres to execute docker-entrypoint-initdb.d/init.sql
