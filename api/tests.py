from django.test import TestCase
from django.urls import reverse
from rest_framework import status, test
from unittest_parametrize import ParametrizedTestCase

from .setup_tests import (
    setup_data,
    test_transaction_summary_parameters,
    test_transaction_summary_by_category_parameters,
)


class TransactionSummaryTestCase(ParametrizedTestCase, TestCase):
    def setUp(self):
        self.client = test.APIClient()
        url = reverse('transaction-create')
        response = self.client.post(url, setup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @test_transaction_summary_parameters
    def test_transaction_summary(self, expected_data):
        url = reverse('transaction-summary-by-type-per-user')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    @test_transaction_summary_by_category_parameters
    def test_transaction_summary_by_category(self, user_email, expected_data):
        url = reverse('transaction-category-summary')
        response = self.client.get(url, {'user_email': user_email})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
