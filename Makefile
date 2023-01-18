lint:
	poetry run flake8 task_manager

test:
	poetry run pytest --cov=task_manager

test-coverage:
	poetry run pytest --cov=task_manager --cov-report xml

install:
	poetry install

selfcheck:
	poetry check

check: selfcheck test lint

dev:
	poetry run python manage.py runserver

#start:
#
