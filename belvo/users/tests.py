from model_bakery import baker
from rest_framework import status

from django.test import TestCase
from django.urls import reverse

from belvo.users.models import User
from belvo.users.serializers import UserSerializer
from belvo.transactions.models import Transaction


class UserTests(TestCase):
    def test_list_users_successfully(self):
        self.assertEqual(0, User.objects.count())
        user = baker.make("users.User")
        self.assertEqual(1, User.objects.count())

        url = reverse("users:user")
        response = self.client.get(path=url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))

        expected_data = [
            {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "age": user.age,
            }
        ]
        self.assertEqual(expected_data, response.data)

    def test_create_user_successfully(self):
        self.assertEqual(0, User.objects.count())

        user_sample = baker.prepare("users.User")

        url = reverse("users:user")
        response = self.client.post(
            path=url,
            content_type="application/json",
            data=UserSerializer(user_sample).data,
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, User.objects.count())

        expected_data = {
            "name": user_sample.name,
            "email": user_sample.email,
            "age": user_sample.age,
        }

        self.assertTrue(
            all(item in response.data.items() for item in expected_data.items())
        )


class UserBalance(TestCase):
    def test_get_account_balance_without_date_range(self):

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

        url = reverse("users:user_balance", kwargs={"pk": user.id})
        response = self.client.get(path=url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected_data = [
            {
                "account": "C00099",
                "balance": "1738.87",
                "total_inflow": "2500.72",
                "total_outflow": "-761.85",
            },
            {
                "account": "S00012",
                "balance": "150.72",
                "total_inflow": "150.72",
                "total_outflow": "0.00",
            },
        ]
        self.assertEqual(expected_data, response.data)

    def test_get_account_balance_with_start_date(self):
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

        url = reverse("users:user_balance", kwargs={"pk": user.id})
        response = self.client.get(path=url, data={"start": "2020-01-12"})
        expected_data = [
            {
                "account": "C00099",
                "balance": "-560.00",
                "total_inflow": "0.00",
                "total_outflow": "-560.00",
            },
        ]
        self.assertEqual(expected_data, response.data)

    def test_get_account_balance_with_end_date(self):
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

        url = reverse("users:user_balance", kwargs={"pk": user.id})
        response = self.client.get(path=url, data={"end": "2020-01-05"})
        expected_data = [
            {
                "account": "C00099",
                "balance": "-51.13",
                "total_inflow": "0.00",
                "total_outflow": "-51.13",
            },
        ]
        self.assertEqual(expected_data, response.data)

    def test_get_account_balance_with_start_date_and_end_date(self):
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

        url = reverse("users:user_balance", kwargs={"pk": user.id})
        response = self.client.get(
            path=url, data={"start": "2020-01-05", "end": "2020-01-12"}
        )
        expected_data = [
            {
                "account": "C00099",
                "balance": "2350.00",
                "total_inflow": "2500.72",
                "total_outflow": "-150.72",
            },
            {
                "account": "S00012",
                "balance": "150.72",
                "total_inflow": "150.72",
                "total_outflow": "0.00",
            },
        ]
        self.assertEqual(expected_data, response.data)


class UserSummary(TestCase):
    def test_get_account_summary(self):

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

        url = reverse("users:user_summary", kwargs={"pk": user.id})
        response = self.client.get(path=url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected_data = {
            "inflow": {"salary": "2500.72", "savings": "150.72"},
            "outflow": {
                "groceries": "-51.13",
                "rent": "-560.00",
                "transfer": "-150.72",
            },
        }
        self.assertEqual(expected_data, response.data)
