import json

from rest_framework import status
from rest_framework.test import APITransactionTestCase


class UsersAPITests(APITransactionTestCase):
    reset_sequences = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.users_endpoint = '/api/users/'
        cls.me_url = cls.users_endpoint + 'me/'
        cls.login_endpoint = '/api/auth/token/login/'
        cls.yet_another_user_profile = cls.users_endpoint + '2/'
        cls.not_existing_user_profile = cls.users_endpoint + '3/'

        cls.empty_users_list = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        }

        cls.not_empty_users_list = {
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

        cls.user_data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "some_strong_psw"
        }

        cls.login_data = {
            "email": "vpupkin@yandex.ru",
            "password": "some_strong_psw"
        }

        cls.yet_another_user_data = {
            "email": "yet_another_vpupkin@yandex.ru",
            "username": "yet_another_vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "yet_another_strong_psw"
        }

        cls.correct_response_data_after_reg = {
            "email": "vpupkin@yandex.ru",
            'id': 1,
            "username": "vasya.pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин"
        }

        cls.error_msg_for_duplicate_user = {
            "email": ["This field must be unique."],
            "username": ["This field must be unique."]
        }

    def create_user(self):
        return self.client.post(self.users_endpoint, self.user_data)

    def create_yet_another_user(self):
        return self.client.post(
            self.users_endpoint,
            self.yet_another_user_data
        )

    def create_and_authorize_user(self):
        self.create_user()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user_obtain_token()
        )

    def user_obtain_token(self):
        response = self.client.post(self.login_endpoint, self.login_data)
        return json.loads(response.content).get('auth_token')

    def test_empty_users_list(self):
        response = self.client.get(self.users_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.empty_users_list
        )

    def test_create_user(self):
        response = self.create_user()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            json.loads(response.content),
            self.correct_response_data_after_reg
        )

    def test_not_empty_users_list(self):
        self.create_user()
        response = self.client.get(self.users_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.not_empty_users_list
        )

    def test_not_duplicate_user(self):
        self.create_user()
        response = self.create_user()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            self.error_msg_for_duplicate_user
        )

    def test_me_not_allow_for_anonymous(self):
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_me_allow_for_authenticated(self):
        self.create_and_authorize_user()
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_another_user_profile_allow_for_authorized(self):
        self.create_and_authorize_user()
        self.create_yet_another_user()
        response = self.client.get(self.yet_another_user_profile)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_existing_user_return_404(self):
        self.create_and_authorize_user()
        response = self.client.get(self.not_existing_user_profile)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

