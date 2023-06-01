# Belvo Backend (API) Case Challenge

This project implements a simple API to register users' transactions and have an overview of how they are using their money.

## Running the project locally

To run the project locally, you'll need to have **Python** installed. Make sure to create an isolated virtual environment and activate it. Install the project dependencies by running:

```bash
make install
```

You'll also need to have **PostgreSQL** installed and running. Create a database and create an `.env` file in the project root directory with the content listed by the file `.example.env`. Then, run the server:

```bash
make start
```

### Running the tests

To run the tests, execute the comand:

```bash
make test
```

## Running the project locally with Docker

Alternatively, to run the project locally using docker, you need to have `Docker` and `docker-compose` installed.

Simply run the following command:

```bash
make docker-run
```

## API Documentation

There are three endpoints available:

- `POST /api/transactions/`: Creates new users' transactions. The request body must contain the following fields, or a list of objects with the same fields:
    - `reference`: The transaction reference. Must be unique and contain 6 alphanumeric digits.
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
