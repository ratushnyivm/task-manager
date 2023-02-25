start:
	poetry run python manage.py runserver

lint:
	poetry run flake8 task_manager

requirements:
	poetry export -f requirements.txt --without-hashes -o requirements.txt

makemessages:
	poetry run django-admin makemessages --ignore="static" --ignore=".venv" -l ru

compilemessages:
	poetry run django-admin compilemessages --ignore="static" --ignore=".venv"

