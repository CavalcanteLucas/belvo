from model_bakery import baker

from django.test import TestCase
from django.db.utils import IntegrityError

from belvo.transactions.models import Transaction, TransactionTypes


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
            baker.make("Transaction", type="OTHER")

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
