import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from users.views.user_view import (follow_not_exist_error, follow_twice_error,
                                   self_follow_error)


class UsersAPITests(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.users_endpoint = '/api/users/'
        cls.subscriptions_endpoint = '/api/users/subscriptions/'
        cls.self_follow_endpoint = '/api/users/1/subscribe/'
        cls.follow_endpoint = '/api/users/2/subscribe/'
        cls.not_existing_following_user = '/api/users/3/subscribe/'

        cls.user = User.objects.create_user(
            email='vpupkin@yandex.ru',
            username='vasya.pupkin',
            first_name='Вася',
            last_name='Пупкин',
            password='some_strong_psw'
        )

        cls.yet_another_user = User.objects.create_user(
            email='yet_another_vpupkin@yandex.ru',
            username='yet_another_vasya.pupkin',
            first_name='Вася',
            last_name='Пупкин',
            password='yet_another_strong_psw'
        )

        following_user_obj = User.objects.get(pk=2)

        cls.correct_created_response = {
            "email": following_user_obj.email,
            "id": following_user_obj.pk,
            "username": following_user_obj.username,
            "first_name": following_user_obj.first_name,
            "last_name": following_user_obj.last_name,
            "is_subscribed": True,
            "recipes": [],
            "recipes_count": 0
        }

        cls.correct_follow_twice_error = {
            "errors": follow_twice_error
        }

        cls.correct_self_follow_error = {
            "errors": self_follow_error
        }

        cls.correct_follow_not_exist_error = {
            "errors": follow_not_exist_error
        }

        cls.empty_following_list = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        }

        cls.token = Token.objects.create(user=cls.user)

    def authorize_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + str(self.token)
        )

    def test_anonymous_not_allowed(self):
        response = self.client.get(self.subscriptions_endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authorized_allowed(self):
        self.authorize_user()
        response = self.client.get(self.subscriptions_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.empty_following_list
        )

    def test_subscribe_not_allowed_for_anonymous(self):
        response = self.client.post(self.follow_endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_subscribe_for_not_existing_user(self):
        self.authorize_user()
        response = self.client.post(self.not_existing_following_user)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_subscribe_allow_for_authorized(self):
        self.authorize_user()
        response = self.client.post(self.follow_endpoint)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content),
            self.correct_created_response
        )

    def test_not_subscribed_twice(self):
        self.authorize_user()
        self.client.post(self.follow_endpoint)
        response = self.client.post(self.follow_endpoint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            self.correct_follow_twice_error
        )

    def test_not_self_followed(self):
        self.authorize_user()
        response = self.client.post(self.self_follow_endpoint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            self.correct_self_follow_error
        )

    def test_not_unsubscribe_for_not_existing_user(self):
        self.authorize_user()
        response = self.client.delete(self.not_existing_following_user)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_unsubscribe_allow_for_authorized(self):
        self.authorize_user()
        self.client.post(self.follow_endpoint)
        response = self.client.delete(self.follow_endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_unsubscribing_not_allow_for_anonymous(self):
        response = self.client.delete(self.follow_endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_unsubscribe_if_not_subscribed(self):
        self.authorize_user()
        response = self.client.delete(self.follow_endpoint)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            self.correct_follow_not_exist_error
        )
