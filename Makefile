.PHONY: help install install-dev test format lint type-check clean run docker-build docker-run pre-commit

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make install-dev  - Install development dependencies"
	@echo "  make test         - Run tests"
	@echo "  make format       - Format code with black and isort"
	@echo "  make lint         - Run linting with flake8"
	@echo "  make type-check   - Run type checking with mypy"
	@echo "  make clean        - Remove cache files"
	@echo "  make run          - Run the application"
	@echo "  make docker-build - Build Docker image"
	@echo "  make docker-run   - Run Docker container"
	@echo "  make pre-commit   - Run pre-commit hooks"

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest tests/ -v --cov=utils --cov-report=html --cov-report=term

format:
	black .
	isort .

lint:
	flake8 . --max-line-length=88 --extend-ignore=E203,W503

type-check:
	mypy . --ignore-missing-imports

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete

run:
	streamlit run app.py

docker-build:
	docker build -t product-info-extractor .

docker-run:
	docker-compose up --build

pre-commit:
	pre-commit run --all-files