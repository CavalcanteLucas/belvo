from model_bakery import baker
from rest_framework import status

from django.test import TestCase
from django.urls import reverse


from belvo.users.models import User
from belvo.users.serializers import UserSerializer


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
                "id": 1,
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
            "id": 1,
            "name": user_sample.name,
            "email": user_sample.email,
            "age": user_sample.age,
        }

        self.assertEqual(expected_data, response.data)
