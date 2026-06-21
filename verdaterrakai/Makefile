.PHONY: setup test eval lint format run build

setup:
	pip install -e ".[dev,test]"

test:
	pytest tests/

eval:
	python tests/evals/eval_runner.py

lint:
	flake8 src/ tests/
	isort --check-only src/ tests/
	black --check src/ tests/

format:
	isort src/ tests/
	black src/ tests/

run:
	uvicorn verdaterrakai.app.main:app --host 0.0.0.0 --port 8080 --reload

build:
	docker build -t verdaterrakai .
