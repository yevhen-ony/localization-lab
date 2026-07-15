
.PHONY: build up down run

build:
	docker build -t lab:latest -f docker/Dockerfile .

up:
	docker compose up

down:
	docker compose down -v

run:
	python -m src.main

