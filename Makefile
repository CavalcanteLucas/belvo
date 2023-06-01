migrate:
	python manage.py migrate

build:
	pip install -r requirements.txt
	make migrate
	chmod +x ./entrypoint.sh
	./entrypoint.sh

run:
	python manage.py runserver 0.0.0.0:8000

test:
	python manage.py test

docker-run:
	docker-compose up --build
