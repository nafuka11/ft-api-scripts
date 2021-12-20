.PHONY: lint
lint: ## Lint with black, flake8, mypy and isort
	poetry run black --check .
	poetry run flake8 .
#	poetry run mypy .
	poetry run isort --diff .

.PHONY: format
format: ## Format with black and isort
	poetry run black .
	poetry run isort .

.PHONY: help
help: ## Show this message
	@echo "Target lists:"
	@grep -E '^[a-zA-Z_-]+\t*:.*?## .*$$' Makefile | awk 'BEGIN {FS = "\t*:.*?## "}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'
