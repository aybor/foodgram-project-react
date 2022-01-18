import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.serializers import CustomUserCreateSerializer


class RegistrationTestCase(APITestCase):


    correct_response_data_after_reg = {
        "email": "vpupkin@yandex.ru",
        "username": "vasya.pupkin",
        "first_name": "Вася",
        "last_name": "Пупкин"
    }

    def test_registration(self):
        data = {
          "email": "vpupkin@yandex.ru",
          "username": "vasya.pupkin",
          "first_name": "Вася",
          "last_name": "Пупкин",
          "password": "qwedcxzas"
        }
        response = self.client.post('/api/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        for key, value in self.correct_response_data_after_reg.items():
            with self.subTest(field=key):
                self.assertIn(key, response.data.keys())
                self.assertIn(value, response.data.values())
        self.assertNotIn("password", response.data.keys())


