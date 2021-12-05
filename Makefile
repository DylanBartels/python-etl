.PHONY: object-storage postgresql spark


object-storage:
	docker-compose -f object-storage/docker-compose.yml build
	docker-compose -f object-storage/docker-compose.yml up


postgresql:
	docker-compose -f postgresql/docker-compose.yml build
	docker-compose -f postgresql/docker-compose.yml up


spark:
	docker-compose -f spark/docker-compose.yml build
	docker-compose -f spark/docker-compose.yml up
