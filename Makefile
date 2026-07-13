
.PHONY: build up

build:
	docker build -t viewer:latest -f docker/viewer.Dockerfile .

up:
	docker compose up

