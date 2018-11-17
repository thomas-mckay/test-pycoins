SHELL:=/bin/bash

runserver:
	DJANGO_SETTINGS_MODULE=pycoins.settings.local python manage.py runserver 8080

makemigrations:
	DJANGO_SETTINGS_MODULE=pycoins.settings.local python manage.py makemigrations

migrate:
	DJANGO_SETTINGS_MODULE=pycoins.settings.local python manage.py migrate

dependencies:
	pip install --upgrade pip
	pip install -r requirements/dev.txt

test:
	pytest tests/ -vvs --cov-report term --cov=pycoins --color=yes

test-lf:
	pytest tests/ -vvs --lf
