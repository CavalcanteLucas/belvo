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

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
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

        self.assertEqual(expected_data, response.data)

    def test_create_bulk_transactions_successfully(self):
        baker.make("users.User")

        self.assertEqual(0, Transaction.objects.count())

        transactions_bulk_sample = [
            {
                "reference": "000052",
                "account": "C00099",
                "date": "2020-01-10",
                "amount": "2500.72",
                "type": "inflow",
                "category": "salary",
                "user_id": 1,
            },
            {
                "reference": "000053",
                "account": "C00099",
                "date": "2020-01-10",
                "amount": "-150.72",
                "type": "outflow",
                "category": "transfer",
                "user_id": 1,
            },
        ]

        url = reverse("transactions:transaction")

        response = self.client.post(
            path=url,
            content_type="application/json",
            data=transactions_bulk_sample,
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, Transaction.objects.count())

        self.assertEqual(transactions_bulk_sample, response.data)

    def test_create_bulk_transactions_successfully_even_with_repeated_transactions(
        self,
    ):
        baker.make("users.User")

        self.assertEqual(0, Transaction.objects.count())

        transactions_bulk_sample = [
            {
                "reference": "000052",
                "account": "C00099",
                "date": "2020-01-10",
                "amount": "2500.72",
                "type": "inflow",
                "category": "salary",
                "user_id": 1,
            },
            {
                "reference": "000052",
                "account": "C00099",
                "date": "2020-01-10",
                "amount": "2500.72",
                "type": "inflow",
                "category": "salary",
                "user_id": 1,
            },
        ]

        url = reverse("transactions:transaction")

        response = self.client.post(
            path=url,
            content_type="application/json",
            data=transactions_bulk_sample,
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Transaction.objects.count())

        self.assertEqual(transactions_bulk_sample, response.data)
