lint:
	poetry run flake8 task_manager

test:
	poetry run python3 manage.py test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage report -m --include=task_manager/*
	poetry run coverage xml --include=task_manager/*

install:
	poetry install

selfcheck:
	poetry check

check: selfcheck test-coverage lint

dev:
	poetry run python manage.py runserver

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) task_manager.wsgi

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

shell:
	poetry run python manage.py shell_plus --ipython

makemessages:
	 django-admin makemessages --ignore="static" --ignore=".env" -l ru

compilemessages:
	django-admin compilemessages
