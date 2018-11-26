SHELL:=/bin/bash

runserver:
	DJANGO_SETTINGS_MODULE=pycoins.settings.local python manage.py runserver 8080

shell-plus:
	DJANGO_SETTINGS_MODULE=pycoins.settings.local python manage.py shell_plus --print-sql

makemigrations:
	DJANGO_SETTINGS_MODULE=pycoins.settings.local python manage.py makemigrations

migrate:
	DJANGO_SETTINGS_MODULE=pycoins.settings.local python manage.py migrate

notify:
	DJANGO_SETTINGS_MODULE=pycoins.settings.local python manage.py notify

dependencies:
	pip install --upgrade pip
	pip install -r requirements/dev.txt

test:
	DJANGO_SETTINGS_MODULE=pycoins.settings.test coverage run --source='./pycoins' manage.py test
	coverage report -m

test-lf:
	pytest tests/ -vvs --lf
