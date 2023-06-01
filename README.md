# Belvo Backend (API) Case Challenge

This project implements a simple API to register users' transactions and have an overview of how they are using their money.

## Running the project locally

To run the project locally, you'll need to have **Python** installed. You'll also need to have **PostgreSQL** installed and running.

First, create an `.env` file in the project root directory. You can use the `.example.env` file as a template.

Make sure to create an isolated virtual environment and activate it. Then, install the project dependencies by running:

```bash
make build
```

You can run the project by executing:

```bash
make start
```

## Running the tests

To run the tests, execute the comand:

```bash
make test
```

## Running the project locally with Docker

Alternatively, to run the project locally using Docker, you need to have `Docker` and `docker-compose` installed.

Simply run the following command:

```bash
make docker-run
```

## Accessing the API

The project will be served at `http://localhost:8000/`. You can access the Django admin interface at `http://localhost:8000/admin/` to manage the `Transactions`. Please notice that a superuser is required to access the admin interface.

For convenience, a user with admin privileges will be automatically created if you have set the `DJANGO_SUPERUSER`-related environment variables in the `.env` file. Refer to the `.example.env` file for more information. The credentials for the admin user in the dockerized application are listed in the `.docker-env` file.

Also notice that there is no index page available. Refer to the [API Documentation](#api-documentation) section for more information on the available routes.

## API Documentation

There are three endpoints available:

- `POST /api/transactions/`: Creates new users' transactions. The request body must contain the following fields, or a list of objects with the same fields:
    - `reference`: The transaction reference. Must be unique for each `user_email` and it must contain 6 alphanumeric digits.
    - `date`: The transaction date.
    - `amount`: The transaction amount.
    - `type`: The transaction type. Must be either **inflow** or **outflow**.
    - `category`: The transaction category.
    - `user_email`: The user email.

- `GET /api/transactions/summary/type/`: Returns a summary of each user's transactions grouped by type. It shows the total inflow and total outflow per user. The response body will be a list of objects with the following fields:
    - `user_email`: The user email.
    - `inflow`: The sum of all inflow transactions.
    - `outflow`: The sum of all outflow transactions.

- `GET /api/transactions/summary/?user_email=<user@email.com>`: Returns a users' summary by category that shows the sum of amounts per transaction category. The response will be an object with:
    - `inflow`: An object with the sum of transactions for each **inflow** category.
    - `outflow`: An object with the sum of transactions for each **outflow** category.

## Author

Developed by [Lucas Cavalcante](https://github.com/CavalcanteLucas).
