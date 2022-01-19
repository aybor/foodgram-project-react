import json

from rest_framework import status
from rest_framework.test import APITestCase


class UsersAPITests(APITestCase):

    users_endpoint = '/api/users/'
    me_url = users_endpoint + 'me/'
    login_endpoint = '/api/auth/token/login/'
    yet_another_user_profile = users_endpoint + '2/'
    not_existing_user_profile = users_endpoint + '3/'

    empty_users_list = {
        "count": 0,
        "next": None,
        "previous": None,
        "results": []}

    not_empty_users_list = {
        "count": 1,
        "next": None,
        "previous": None,
        "results": [
             {
                 "email": "vpupkin@yandex.ru",
                 "id": 1,
                 "username": "vasya.pupkin",
                 "first_name": "Вася",
                 "last_name": "Пупкин",
                 "is_subscribed": False
             }
        ]
    }

    user_data = {
        "email": "vpupkin@yandex.ru",
        "username": "vasya.pupkin",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "password": "some_strong_psw"
    }

    login_data = {
        "email": "vpupkin@yandex.ru",
        "password": "some_strong_psw"
    }

    yet_another_user_data = {
        "email": "yet_another_vpupkin@yandex.ru",
        "username": "yet_another_vasya.pupkin",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "password": "yet_another_strong_psw"
    }

    correct_response_data_after_reg = {
        "email": "vpupkin@yandex.ru",
        'id': 1,
        "username": "vasya.pupkin",
        "first_name": "Вася",
        "last_name": "Пупкин"
    }

    error_msg_for_duplicate_user = {
        "email": ["This field must be unique."],
        "username": ["This field must be unique."]
    }

    def test_users(self):

        response = self.client.get(self.users_endpoint)
        with self.subTest(test='empty users list'):
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )
            self.assertEqual(
                json.loads(response.content),
                self.empty_users_list
            )

        response = self.client.post(self.users_endpoint, self.user_data)
        with self.subTest(test='create user'):
            self.assertEqual(
                response.status_code,
                status.HTTP_201_CREATED
            )
            self.assertEqual(
                json.loads(response.content),
                self.correct_response_data_after_reg
            )

        response = self.client.get(self.users_endpoint)
        with self.subTest(test='not empty users list'):
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )
            self.assertEqual(
                json.loads(response.content),
                self.not_empty_users_list
            )

        response = self.client.post(self.users_endpoint, self.user_data)
        with self.subTest(test='not duplicated'):
            self.assertEqual(
                response.status_code,
                status.HTTP_400_BAD_REQUEST
            )
        with self.subTest(test='correct error'):
            self.assertEqual(
                json.loads(response.content),
                self.error_msg_for_duplicate_user
            )

        self.client.post(self.users_endpoint, self.yet_another_user_data)
        response = self.client.get(self.me_url)
        with self.subTest(test='me not allow for anonymous'):
            self.assertEqual(
                response.status_code,
                status.HTTP_401_UNAUTHORIZED
            )

        response = self.client.post(self.login_endpoint, self.login_data)
        token = json.loads(response.content)['auth_token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = self.client.get(self.me_url)
        with self.subTest(test='me allow for authorized'):
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )

        response = self.client.get(self.yet_another_user_profile)
        with self.subTest(test='another user profile allow for authorized'):
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )

        response = self.client.get(self.not_existing_user_profile)
        with self.subTest(test='not existing user return 404'):
            self.assertEqual(
                response.status_code,
                status.HTTP_404_NOT_FOUND
            )

