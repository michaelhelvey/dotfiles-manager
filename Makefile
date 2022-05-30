.PHONY: all

sync:
	@pipenv run python source/main.py sync

push:
	@pipenv run python source/main.py push

test:
	@pipenv run pytest

