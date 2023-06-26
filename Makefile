docker-build:
	docker buildx build \
	--build-arg BASE_LAYER=base-dev \
	-t llm-gateway-backend .
	docker buildx build \
	-t llm-gateway-frontend ./front_end

docker-test:
	docker buildx build \
	--build-arg BASE_LAYER=base-dev \
	--target test-suite \
	-t llm-gateway-test .

	docker run -ti llm-gateway-test pytest $(TEST_OPTIONS)

docker-run:
	docker-compose -p llm-gateway -f docker-compose.yml up --detach

browse:
	open http://localhost:3000

browse-api:
	open http://localhost:5000/api/docs

clean:
	docker-compose -p llm-gateway -f docker-compose.yml down
	docker-compose rm  # force postgres to execute docker-entrypoint-initdb.d/init.sql
