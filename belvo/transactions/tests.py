from model_bakery import baker

from django.test import TestCase

from belvo.transactions.models import Transaction


class TransactionTests(TestCase):
    def test_that_a_transaction_reference_is_unique(self):
        return
