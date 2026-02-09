.PHONY: help install install-dev run test lint format clean docker-build docker-up docker-down docker-logs

# Default target
help:
	@echo "Available commands:"
	@echo "  make install       - Install dependencies with Poetry"
	@echo "  make install-dev   - Install dev dependencies with Poetry"
	@echo "  make run           - Run the bot locally"
	@echo "  make test          - Run tests"
	@echo "  make lint          - Run type checking with mypy"
	@echo "  make format        - Format code with black"
	@echo "  make clean         - Remove generated files"
	@echo ""
	@echo "Docker commands:"
	@echo "  make docker-build  - Build Docker image"
	@echo "  make docker-up     - Start bot in Docker"
	@echo "  make docker-down   - Stop Docker containers"
	@echo "  make docker-logs   - View Docker logs"
	@echo "  make docker-shell  - Open shell in container"

# Poetry installation
install:
	poetry install --no-dev

install-dev:
	poetry install

# Run the bot
run:
	poetry run python main.py

# Testing
test:
	poetry run pytest -v

# Linting
lint:
	poetry run mypy app/

# Formatting
format:
	poetry run black app/ main.py

# Cleaning
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.log" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov/
	rm -rf temp/*.png

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-shell:
	docker-compose exec bot /bin/bash

docker-restart:
	docker-compose restart

# Combined commands
dev: install-dev
	@echo "Development environment ready!"

prod-docker: docker-build docker-up
	@echo "Bot running in Docker!"
	@echo "View logs with: make docker-logs"
