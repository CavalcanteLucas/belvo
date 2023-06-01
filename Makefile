install:
	pip install -r requirements.txt

migrate:
	python manage.py migrate

run:
	python manage.py runserver 0.0.0.0:8000

start:
	make migrate
	make run

test:
	python manage.py test

docker-run:
	docker-compose up --build
