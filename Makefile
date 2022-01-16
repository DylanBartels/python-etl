.PHONY: object-storage spark prefect


object-storage:
	docker-compose -f object-storage/docker-compose.yml build
	docker-compose -f object-storage/docker-compose.yml up


spark:
	docker-compose -f spark/docker-compose.yml build
	docker-compose -f spark/docker-compose.yml up


prefect:
	docker-compose -f prefect/docker-compose.yml build
	docker-compose -f prefect/docker-compose.yml up
