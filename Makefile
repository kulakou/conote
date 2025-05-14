build:
	docker compose -f docker/docker-compose.yaml build
run:
	docker compose -f docker/docker-compose.yaml up
run_backend:
	docker compose -f docker/docker-compose.yaml up backend
run_frontend:
	docker compose -f docker/docker-compose.yaml up frontend
stop:
	docker compose -f docker/docker-compose.yaml stop
