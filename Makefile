build:
	docker compose -f docker/docker-compose.yaml build
run:
	docker compose -f docker/docker-compose.yaml up
stop:
	docker compose -f docker/docker-compose.yaml stop
