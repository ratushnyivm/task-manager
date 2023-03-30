MANAGE := poetry run python3 manage.py

install:
	poetry install

start:
	${MANAGE} runserver

lint:
	poetry run flake8 task_manager

test:
	${MANAGE} test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage xml --omit=*/tests/*,*/migrations/*,*__init__.py,*settings.py
	poetry run coverage report --omit=*/tests/*,*/migrations/*,*__init__.py,*settings.py

requirements:
	poetry export -f requirements.txt --without-hashes -o requirements.txt

makemessages:
	poetry run django-admin makemessages --ignore="static" --ignore=".venv" -l ru

compilemessages:
	poetry run django-admin compilemessages --ignore="static" --ignore=".venv"

migrate:
	${MANAGE} makemigrations
	${MANAGE} migrate

shell:
	${MANAGE} shell

check: lint test requirements

dumpdata:
	${MANAGE} dumpdata --indent 2 > db.json
