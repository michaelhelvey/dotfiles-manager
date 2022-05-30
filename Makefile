.PHONY: all

default:
	@pipenv run python source/main.py

test:
	@pipenv run pytest

