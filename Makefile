build:
	@docker-compose build

stop:
	@docker-compose down --remove-orphans

run: stop build
	@docker-compose up  --remove-orphans

test-build:
	@docker-compose -f docker-compose-dev.yaml build

test: stop test-build
	target=src/tests
	@docker-compose -f docker-compose-dev.yaml up
