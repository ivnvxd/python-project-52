lint:
	poetry run flake8 task_manager

test:
	#poetry run pytest --cov=task_manager
	poetry run python3 manage.py test

test-coverage:
	#poetry run pytest --cov=task_manager --cov-report xml
	poetry run coverage run manage.py test
	poetry run coverage report
	poetry run coverage xml

install:
	poetry install

selfcheck:
	poetry check

check: selfcheck test test-coverage lint

dev:
	poetry run python manage.py runserver

#PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$PORT task_manager.wsgi

migrate:
	poetry run python manage.py makemigrations
	poetry run python manage.py migrate

shell:
	poetry run python manage.py shell_plus --ipython