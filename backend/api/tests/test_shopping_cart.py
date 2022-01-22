import json
import shutil
import tempfile

from django.conf import settings
from django.contrib.auth.models import User
from django.test import override_settings

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITransactionTestCase

from api.models import (Ingredient, Tag)
from api.views.RecipeView import (recipe_already_deleted_msg,
                                  recipe_already_exists_msg)

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class RecipeAPITests(APITransactionTestCase):
    reset_sequences = True

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.shopping_url = "/api/recipes/1/shopping_cart/"
        cls.not_existing_url = "/api/recipes/2/shopping_cart/"
        cls.recipes_endpoint = '/api/recipes/'
        cls.download_cart_url = '/api/recipes/download_shopping_cart/'

        cls.test_recipe_data = {
            "ingredients": [{"id": 1, "amount": 10}],
            "tags": [1],
            "image": "data:image/png;"
                     "base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAA"
                     "AACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4"
                     "bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "test_string",
            "text": "test_string",
            "cooking_time": 1
        }

        cls.json_data = json.dumps(cls.test_recipe_data)

        cls.success_response_fields = [
            'id',
            'name',
            'image',
            'cooking_time'
        ]

        cls.download_text = b'test_ingredient: 10 test\n'

        cls.already_in_cart = {
            'errors': recipe_already_exists_msg
        }
        cls.already_not_in_cart = {
            'errors': recipe_already_deleted_msg
        }

    def authorize_user(self, token):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + str(token)
        )

    def unauthorize_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="")

    def setUp(self):
        self.user = User.objects.create_user(
            email='vpupkin@yandex.ru',
            username='vasya.pupkin',
            first_name='Вася',
            last_name='Пупкин',
            password='some_strong_psw'
        )

        self.tag = Tag.objects.create(
            name='test_tag_name',
            color='#FFFFFF',
            slug='test_tag_slug'
        )

        self.ingredient = Ingredient.objects.create(
            name='test_ingredient',
            measurement_unit='test'
        )
        self.token = Token.objects.create(user=self.user)

        self.authorize_user(self.token)
        self.client.post(
            self.recipes_endpoint,
            content_type='application/json',
            data=self.json_data
        )
        self.unauthorize_user()

    def test_shopping_not_allowed_for_anonymous(self):
        response = self.client.post(self.shopping_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_shopping_allowed_for_authorized(self):
        self.authorize_user(self.token)
        response = self.client.post(self.shopping_url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_keys = json.loads(response.content).keys()
        for field in self.success_response_fields:
            with self.subTest(field=field):
                self.assertIn(field, response_keys)

    def test_not_add_to_cart_twice(self):
        self.authorize_user(self.token)
        self.client.post(self.shopping_url)
        response = self.client.post(self.shopping_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            self.already_in_cart
        )

    def test_del_cart_not_allowed_for_anonymous(self):
        response = self.client.delete(self.shopping_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_del_cart_allowed_for_authorized(self):
        self.authorize_user(self.token)
        self.client.post(self.shopping_url)
        response = self.client.delete(self.shopping_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_not_del_from_cart_twice(self):
        self.authorize_user(self.token)
        response = self.client.delete(self.shopping_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            self.already_not_in_cart
        )

    def test_download_not_allowed_for_anonymous(self):
        self.authorize_user(self.token)
        self.client.post(self.shopping_url)
        self.unauthorize_user()
        response = self.client.get(self.download_cart_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_download_allowed_for_authorized(self):
        self.authorize_user(self.token)
        self.client.post(self.shopping_url)
        response = self.client.get(self.download_cart_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content, self.download_text)
