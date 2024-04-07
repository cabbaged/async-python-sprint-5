.PHONY: run

run:
	docker-compose --env-file=src/.env up --build

stop:
	docker-compose --env-file=src/.env down

migration:
	cd src && alembic upgrade head
