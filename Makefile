start:
	poetry run python manage.py runserver

lint:
	poetry run flake8

requirements:
	poetry export -f requirements.txt --without-hashes -o requirements.txt

