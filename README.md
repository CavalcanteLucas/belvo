# Belvo Backend (API) Case Challenge

This project implements a simple API to register users' transactions and give an overview of how they are using their money.

## Running the project

To run the project locally, you'll need to have `Docker` and `docker-compose` installed.

Simply execute the following command:

```bash
make run
```

## Running the tests

To run the tests exclusively, execute the comand:

```bash
make test
```

## Accessing the API

The project will be served at `http://localhost:8000/`. However, please notice that there is no index page available. Refer to the [API Documentation](#api-documentation) section for more information on the available routes.

You can access the Django admin interface at `http://localhost:8000/admin/` to manage the `Transactions`. For convenience, a user with admin privileges will be automatically created with default credentials `admin:dale`.

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

## Notes

This assignment took me about 6~8 hours to complete.

## Author

Developed by [Lucas Cavalcante](https://github.com/CavalcanteLucas).
