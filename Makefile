SHELL:=/bin/bash

dependencies:
	pip install --upgrade pip
	pip install -r requirements/dev.txt

test:
	pytest tests/ -vvs --cov-report term --cov=pycoins --color=yes

test-lf:
	pytest tests/ -vvs --lf
