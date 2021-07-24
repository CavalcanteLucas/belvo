# Belvo Backend (API) Case Challenge Software

## Prerequisites:
- Have the `python3.8-dev` package installed
- Have Postgres installed and configured

## Installation

- Clone the repository
- Create a virtual environment running Python 3.8
- Activate the virtual environment
- Install the project dependencies
```
pip install -r requirements.txt
```
- Create the database and user on PostgrSQL
```
$  sudo -u postgres psql

postgres=# CREATE USER <POSTGRES_USER> WITH PASSWORD '<POSTGRES_PASSWORD>';
postgres=# ALTER USER <POSTGRES_USER> WITH SUPERUSER;
postgres=# CREATE database <POSTGRES_DB>;
```
- Migrate the database
```
python manage.py makemigrations
python manage.py migrate
```
- Make sure to have a superuser created, in case you want to access the admin. Follow the instructions after run:
```
python manage.py createsuperuser
```

## Usage

- Run the project
```
python manage.py runserver
```
- Go the the browser at `http://localhost:8000/` and access the available endpoints:
  - `api/users/`
    - **GET**: lists all users
    - **POST**: create user
  - `api/transactions/`
    - **POST**: create transaction (input can be a single transaction or a list of transactions)
  - `api/users/<user_id>`
    - **GET**: display information of user with `<user_id>`
  - `api/users/<user_id>/balance/`
    - **GET**: display overall balance of user with `<user_id>`
  - `api/users/<user_id>/balance/?start=yyyy-mm-aa`
    - **GET**: display balance of user with `<user_id>` from start date `yyyy-mm-aa` to today
  - `api/users/<user_id>/balance/?start=yyyy-mm-aa&end=yyyy-mm-aa`
    - **GET**: display balance of user with `<user_id>` from start date `yyyy-mm-aa` to end date `yyyy-mm-aa`
  - `api/users/<user_id>/summary/`
    - **GET**: display inflow / outflow summary of user with `<user_id>`

## Testing

- Run the test suit
```
python manage.py test
```

## Docker
- Make sure to have `docker-compose` installed
- Run the project
```
docker-compose up --build
```
- Edit `settings.py` with correct `HOST`, `NAME` or any other database information
- Make sure to have ownership of the db. Optionally, in the project directory, you can run
```
sudo chown -R $USER:$USER .
```
- Go the the browser at `http://localhost:8000/` and access the available endpoints
- To execute the test suit from docker compose, run
```
docker-compose run web python manage.py test
```
