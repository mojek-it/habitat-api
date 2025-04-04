# Makefile for Docker Compose Development Environment

COMPOSE_CMD := docker compose

# Default target
.PHONY: help
help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@echo "  build        Build or rebuild services"
	@echo "  up           Start services in the background"
	@echo "  down         Stop services"
	@echo "  logs         Follow log output"
	@echo "  ps           List containers"
	@echo "  shell        Start a shell in the web container"
	@echo "  celery-shell Start a shell in the celery container"
	@echo "  migrate      Run database migrations"
	@echo "  makemigrations Create new database migrations"
	@echo "  collectstatic Collect static files"
	@echo "  install      Install/update Python dependencies"
	@echo "  test         Run tests using pytest"
	@echo "  black        Format code using Black"
	@echo "  pre-commit   Install pre-commit hooks"
	@echo "  clean        Remove stopped containers and dangling images"
	@echo "  prune        Remove all unused containers, networks, images, and volumes"

# Build or rebuild services
.PHONY: build
build:
	$(COMPOSE_CMD) build

# Start services in the background
.PHONY: up
up:
	$(COMPOSE_CMD) up -d

# Stop services
.PHONY: down
down:
	$(COMPOSE_CMD) down

# Follow log output
.PHONY: logs
logs:
	$(COMPOSE_CMD) logs -f

# List containers
.PHONY: ps
ps:
	$(COMPOSE_CMD) ps

# Start a shell in the web container
.PHONY: shell
shell:
	$(COMPOSE_CMD) exec web /bin/bash

# Start a shell in the celery container
.PHONY: celery-shell
celery-shell:
	$(COMPOSE_CMD) exec celery /bin/bash

# Run database migrations
.PHONY: migrate
migrate:
	$(COMPOSE_CMD) exec web python manage.py migrate

# Create new database migrations
.PHONY: makemigrations
makemigrations:
	$(COMPOSE_CMD) exec web python manage.py makemigrations $(ARGS)

# Collect static files
.PHONY: collectstatic
collectstatic:
	$(COMPOSE_CMD) exec web python manage.py collectstatic --noinput

# Install/update Python dependencies (inside the container)
.PHONY: install
install:
	$(COMPOSE_CMD) exec web pip install -r requirements.txt
# Run tests
.PHONY: test
test:
	$(COMPOSE_CMD) exec web pytest

# Format code using Black
.PHONY: black
black:
	$(COMPOSE_CMD) exec web black . --exclude=migrations

# Install pre-commit hooks
.PHONY: pre-commit
pre-commit:
	$(COMPOSE_CMD) exec web pre-commit install

# Remove stopped containers and dangling images
# Remove stopped containers and dangling images
.PHONY: clean
clean:
	podman container prune -f
	podman image prune -f

# Remove all unused containers, networks, images, and volumes
.PHONY: prune
prune:
	podman system prune -a -f --volumes

# Ensure environment variables are loaded if .env file exists
# Include .env file if it exists
ifneq (,$(wildcard ./.env))
    include .env
    export
endif