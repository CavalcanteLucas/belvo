from model_bakery import baker
from rest_framework import status

from django.test import TestCase
from django.db.utils import IntegrityError
from django.urls import reverse

from belvo.transactions.models import Transaction, TransactionTypes
from belvo.transactions.serializers import TransactionSerializer


class TransactionTests(TestCase):
    def test_that_a_transaction_reference_is_unique(self):
        self.assertEqual(0, Transaction.objects.count())
        transaction_sample = baker.make(
            "Transaction", type=TransactionTypes.OUTFLOW, amount="-1"
        )
        self.assertEqual(1, Transaction.objects.count())

        with self.assertRaises(IntegrityError):
            baker.make(
                "Transaction",
                type=TransactionTypes.OUTFLOW,
                amount="-2",
                reference=transaction_sample.reference,
            )
            self.assertEqual(1, Transaction.objects.count())

    def test_that_there_are_only_two_types_of_transactions(self):
        self.assertEqual(0, Transaction.objects.count())

        baker.make("Transaction", type=TransactionTypes.OUTFLOW, amount="-1.99")
        self.assertEqual(1, Transaction.objects.count())

        baker.make("Transaction", type=TransactionTypes.INFLOW, amount="3.14")
        self.assertEqual(2, Transaction.objects.count())

        with self.assertRaises(IntegrityError):
            baker.make("Transaction", type="other")

    def test_that_all_outflow_transactions_amounts_are_negative_decimal_numbers(self):
        self.assertEqual(0, Transaction.objects.count())
        baker.make("Transaction", type=TransactionTypes.OUTFLOW, amount="-1.99")
        self.assertEqual(1, Transaction.objects.count())
        with self.assertRaises(IntegrityError):
            baker.make("Transaction", type=TransactionTypes.OUTFLOW, amount="2.00")
            self.assertEqual(1, Transaction.objects.count())

    def test_that_all_inflow_transactions_amounts_are_positive_decimal_numbers(self):
        self.assertEqual(0, Transaction.objects.count())
        baker.make("Transaction", type=TransactionTypes.INFLOW, amount="1.99")
        self.assertEqual(1, Transaction.objects.count())
        with self.assertRaises(IntegrityError):
            baker.make("Transaction", type=TransactionTypes.INFLOW, amount="-0.10")
            self.assertEqual(1, Transaction.objects.count())

    def test_create_transaction_successfully(self):
        user = baker.make("users.User")

        self.assertEqual(0, Transaction.objects.count())

        transaction_sample = baker.prepare(
            "Transaction", type=TransactionTypes.INFLOW, amount="1.99", user_id=user
        )

        url = reverse("transactions:transaction")

        response = self.client.post(
            path=url,
            content_type="application/json",
            data=TransactionSerializer(transaction_sample).data,
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, Transaction.objects.count())

        expected_data = {
            "reference": transaction_sample.reference,
            "account": transaction_sample.account,
            "date": str(transaction_sample.date),
            "amount": transaction_sample.amount,
            "type": transaction_sample.type,
            "category": transaction_sample.category,
            "user_id": transaction_sample.user_id.id,
        }

        self.assertTrue(
            all(item in response.data.items() for item in expected_data.items())
        )

    def test_cant_create_transactions_with_repeated_reference(self):
        user = baker.make("users.User")

        self.assertEqual(0, Transaction.objects.count())

        transaction_sample = baker.make(
            "Transaction",
            reference="000051",
            type=TransactionTypes.INFLOW,
            amount="1.99",
            user_id=user,
        )

        url = reverse("transactions:transaction")

        with self.assertRaises(IntegrityError):
            response = self.client.post(
                path=url,
                content_type="application/json",
                data=TransactionSerializer(transaction_sample).data,
            )
            self.assertEqual(
                status.HTTP_500_INTERNAL_SERVER_ERROR, response.status_code
            )

    def test_create_bulk_transactions_successfully(self):
        user = baker.make("users.User")

        self.assertEqual(0, Transaction.objects.count())

        transactions_bulk_sample = [
            {
                "reference": "000052",
                "account": "C00099",
                "date": "2020-01-10",
                "amount": "2500.72",
                "type": "inflow",
                "category": "salary",
                "user_id": user.id,
            },
            {
                "reference": "000053",
                "account": "C00099",
                "date": "2020-01-10",
                "amount": "-150.72",
                "type": "outflow",
                "category": "transfer",
                "user_id": user.id,
            },
        ]

        url = reverse("transactions:transaction")

        response = self.client.post(
            path=url,
            content_type="application/json",
            data=transactions_bulk_sample,
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, Transaction.objects.count())
        self.assertEqual(2, len(response.data))

        for transaction in transactions_bulk_sample:
            self.assertEqual(
                1, len(Transaction.objects.filter(reference=transaction["reference"]))
            )

    def test_create_bulk_transactions_successfully_even_with_repeated_transactions(
        self,
    ):
        user = baker.make("users.User")

        self.assertEqual(0, Transaction.objects.count())

        transactions_bulk_sample = [
            {
                "reference": "000052",
                "account": "C00099",
                "date": "2020-01-10",
                "amount": "2500.72",
                "type": "inflow",
                "category": "salary",
                "user_id": user.id,
            },
            {
                "reference": "000052",
                "account": "C00099",
                "date": "2020-01-10",
                "amount": "2500.72",
                "type": "inflow",
                "category": "salary",
                "user_id": user.id,
            },
        ]

        url = reverse("transactions:transaction")

        response = self.client.post(
            path=url,
            content_type="application/json",
            data=transactions_bulk_sample,
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, Transaction.objects.count())
        self.assertEqual(1, len(response.data))

        for transaction in transactions_bulk_sample:
            self.assertEqual(
                1, len(Transaction.objects.filter(reference=transaction["reference"]))
            )

    def test_create_bulk_transactions_ignore_conflicts_with_saved_data(self):
        user = baker.make("users.User")

        self.assertEqual(0, Transaction.objects.count())

        transaction_sample = {
            "reference": "000052",
            "account": "C00099",
            "date": "2020-01-10",
            "amount": "2500.72",
            "type": "inflow",
            "category": "salary",
            "user_id": user.id,
        }

        baker.make(
            "Transaction",
            reference=transaction_sample["reference"],
            account=transaction_sample["account"],
            date=transaction_sample["date"],
            amount=transaction_sample["amount"],
            type=transaction_sample["type"],
            category=transaction_sample["category"],
            user_id=user,
        )

        self.assertEqual(1, Transaction.objects.count())

        url = reverse("transactions:transaction")
        response = self.client.post(
            path=url,
            content_type="application/json",
            data=[transaction_sample],
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response.data)

    def test_create_bulk_transactions_ignore_conflicts_within_bulk(self):
        user = baker.make("users.User")

        self.assertEqual(0, Transaction.objects.count())

        transactions_bulk_sample = [
            {
                "reference": "000051",
                "account": "C00099",
                "date": "2020-01-03",
                "amount": "-51.13",
                "type": "outflow",
                "category": "groceries",
                "user_id": user.id,
            },
            {
                "reference": "000052",
                "account": "C00099",
                "date": "2020-01-10",
                "amount": "2500.72",
                "type": "inflow",
                "category": "salary",
                "user_id": user.id,
            },
            {
                "reference": "000053",
                "account": "C00099",
                "date": "2020-01-10",
                "amount": "-150.72",
                "type": "outflow",
                "category": "transfer",
                "user_id": user.id,
            },
            {
                "reference": "000054",
                "account": "C00099",
                "date": "2020-01-13",
                "amount": "-560.00",
                "type": "outflow",
                "category": "rent",
                "user_id": user.id,
            },
            {
                "reference": "000051",
                "account": "C00099",
                "date": "2020-01-04",
                "amount": "-51.13",
                "type": "outflow",
                "category": "other",
                "user_id": user.id,
            },
            {
                "reference": "000689",
                "account": "S00012",
                "date": "2020-01-10",
                "amount": "150.72",
                "type": "inflow",
                "category": "savings",
                "user_id": user.id,
            },
        ]

        url = reverse("transactions:transaction")
        response = self.client.post(
            path=url,
            content_type="application/json",
            data=transactions_bulk_sample,
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(5, len(response.data))
        self.assertEqual(5, Transaction.objects.count())

        for transaction in transactions_bulk_sample:
            self.assertEqual(
                1, len(Transaction.objects.filter(reference=transaction["reference"]))
            )

    def test_create_bulk_transactions_ignore_conflicts_within_bulk_and_saved_data(self):

        user = baker.make("users.User")

        self.assertEqual(0, Transaction.objects.count())

        transaction_sample = {
            "reference": "000051",
            "account": "C00099",
            "date": "2020-01-03",
            "amount": "-51.13",
            "type": "outflow",
            "category": "groceries",
            "user_id": 1,
        }

        baker.make(
            "Transaction",
            reference=transaction_sample["reference"],
            account=transaction_sample["account"],
            date=transaction_sample["date"],
            amount=transaction_sample["amount"],
            type=transaction_sample["type"],
            category=transaction_sample["category"],
            user_id=user,
        )

        self.assertEqual(1, Transaction.objects.count())

        transactions_bulk_sample = [
            {
                "reference": "000051",
                "account": "C00099",
                "date": "2020-01-03",
                "amount": "-51.13",
                "type": "outflow",
                "category": "groceries",
                "user_id": user.id,
            },
            {
                "reference": "000052",
                "account": "C00099",
                "date": "2020-01-10",
                "amount": "2500.72",
                "type": "inflow",
                "category": "salary",
                "user_id": user.id,
            },
            {
                "reference": "000053",
                "account": "C00099",
                "date": "2020-01-10",
                "amount": "-150.72",
                "type": "outflow",
                "category": "transfer",
                "user_id": user.id,
            },
            {
                "reference": "000054",
                "account": "C00099",
                "date": "2020-01-13",
                "amount": "-560.00",
                "type": "outflow",
                "category": "rent",
                "user_id": user.id,
            },
            {
                "reference": "000051",
                "account": "C00099",
                "date": "2020-01-04",
                "amount": "-51.13",
                "type": "outflow",
                "category": "other",
                "user_id": user.id,
            },
            {
                "reference": "000689",
                "account": "S00012",
                "date": "2020-01-10",
                "amount": "150.72",
                "type": "inflow",
                "category": "savings",
                "user_id": user.id,
            },
        ]

        url = reverse("transactions:transaction")
        response = self.client.post(
            path=url,
            content_type="application/json",
            data=transactions_bulk_sample,
        )

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(4, len(response.data))
        self.assertEqual(5, Transaction.objects.count())

        for transaction in transactions_bulk_sample:
            self.assertEqual(
                1, len(Transaction.objects.filter(reference=transaction["reference"]))
            )
