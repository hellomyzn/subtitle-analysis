up:
	docker-compose up -d --build
dev:
	docker-compose -f docker-compose-dev.yml up -d --build
build:
	docker-compose build --no-cache --force-rm
stop:
	docker-compose stop
down:
	docker-compose down
	docker-compose -f docker-compose-dev.yml down
restart:
	@make down
	@make up
destroy:
	docker-compose down --rmi all --volumes --remove-orphans
destroy-volumes:
	docker-compose down --volumes
ps:
	docker-compose ps
logs:
	docker-compose logs
python:
	docker-compose exec python bash
vscode:
	docker-compose exec vscode bash
ssh:
	docker-compose exec ssh-stub bash
start:
	@make up
	@make python
