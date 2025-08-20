.PHONY: format test

format:
	ruff format .
	ruff check . --fix

test:
	coverage run manage.py test
	coverage report -m