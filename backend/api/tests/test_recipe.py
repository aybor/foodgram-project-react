import json
import shutil
import tempfile

from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITransactionTestCase


from api.models import (Ingredient,
                        Tag,
                        Recipe)

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


class RecipeAPITests(APITransactionTestCase):
    reset_sequences = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.recipes_endpoint = '/api/recipes/'
        cls.recipes_detail_endpoint = cls.recipes_endpoint + '1/'

        cls.empty_recipes_list = {
            "count": 0,
            "next": None,
            "previous": None,
            "results": []
        }

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

        cls.changed_test_recipe_data = {
            "ingredients": [{"id": 1, "amount": 100}],
            "tags": [1],
            "image": "data:image/png;"
                     "base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAA"
                     "AACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4"
                     "bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJkkk==",
            "name": "another_test_string",
            "text": "another_test_string",
            "cooking_time": 10
        }

        cls.test_recipe_data_without_ingr_tags = {
            "image": "data:image/png;"
                     "base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAA"
                     "AACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4"
                     "bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "test_string",
            "text": "test_string",
            "cooking_time": 1
        }

        cls.json_data = json.dumps(cls.test_recipe_data)
        cls.json_changed_data = json.dumps(cls.changed_test_recipe_data)
        cls.wrong_json_data = json.dumps(cls.test_recipe_data_without_ingr_tags)

        cls.correct_recipe_keys = [
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        ]

        cls.validation_error_response = {
            "name": ["This field is required."],
            "image": ["No file was submitted."],
            "text": ["This field is required."],
            "cooking_time": ["This field is required."]
        }

    def authorize_user(self, token):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + str(token)
        )

    def unauthorize_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        self.user = User.objects.create_user(
            email='vpupkin@yandex.ru',
            username='vasya.pupkin',
            first_name='Вася',
            last_name='Пупкин',
            password='some_strong_psw'
        )
        self.yet_another_user = User.objects.create_user(
            email='yet_another_vpupkin@yandex.ru',
            username='yet_another_vasya.pupkin',
            first_name='Вася',
            last_name='Пупкин',
            password='yet_another_some_strong_psw'
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
        self.another_token = Token.objects.create(
            user=self.yet_another_user
        )

    def test_recipes_allow_for_any(self):
        response = self.client.get(self.recipes_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.empty_recipes_list
        )

    def test_create_recipe_not_allow_for_anonymous(self):
        response = self.client.post(
            self.recipes_endpoint,
            content_type='application/json',
            data=self.json_data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_recipe_not_allowed_for_anonymous(self):
        self.authorize_user(self.token)
        self.client.post(
            self.recipes_endpoint,
            content_type='application/json',
            data=self.json_data
        )
        self.unauthorize_user()
        response = self.client.get(self.recipes_detail_endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_recipe_allowed_for_authorized(self):
        self.authorize_user(self.token)
        self.client.post(
            self.recipes_endpoint,
            content_type='application/json',
            data=self.json_data
        )
        response = self.client.get(self.recipes_detail_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_keys = json.loads(response.content).keys()
        for key in self.correct_recipe_keys:
            with self.subTest(key=key):
                self.assertIn(key, response_keys)

    def test_create_recipe_allow_for_authorized(self):
        self.authorize_user(self.token)
        response = self.client.post(
            self.recipes_endpoint,
            content_type='application/json',
            data=self.json_data
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_validation_for_recipes_create(self):
        self.authorize_user(self.token)
        response = self.client.post(
            self.recipes_endpoint,
            content_type='application/json',
            data={}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            json.loads(response.content),
            self.validation_error_response
        )

    def test_404_for_null_recipe(self):
        self.authorize_user(self.token)
        self.ingredient.delete()
        response = self.client.post(
            self.recipes_endpoint,
            content_type='application/json',
            data=self.json_data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anonymous_cant_delete_recipe(self):
        self.authorize_user(self.token)
        self.client.post(
            self.recipes_endpoint,
            content_type='application/json',
            data=self.json_data
        )
        self.unauthorize_user()
        response = self.client.delete(self.recipes_detail_endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_existing_cant_be_deleted(self):
        self.authorize_user(self.token)
        response = self.client.delete(self.recipes_detail_endpoint)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_author_allow_for_delete(self):
        self.authorize_user(self.token)
        self.client.post(
            self.recipes_endpoint,
            content_type='application/json',
            data=self.json_data
        )
        response = self.client.delete(self.recipes_detail_endpoint)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_not_author_cant_delete(self):
        self.authorize_user(self.token)
        self.client.post(
            self.recipes_endpoint,
            content_type='application/json',
            data=self.json_data
        )
        self.unauthorize_user()
        self.authorize_user(self.another_token)
        response = self.client.delete(self.recipes_detail_endpoint)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_anonymous_cant_patch(self):
        self.authorize_user(self.token)
        self.client.post(
            self.recipes_endpoint,
            content_type='application/json',
            data=self.json_data
        )
        self.unauthorize_user()
        response = self.client.patch(
            self.recipes_detail_endpoint,
            content_type='application/json',
            data=self.json_changed_data
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_existed_cant_be_patched(self):
        self.authorize_user(self.token)
        response = self.client.patch(
            self.recipes_detail_endpoint,
            content_type='application/json',
            data=self.json_changed_data
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_author_can_patch(self):
        self.authorize_user(self.token)
        self.client.post(
            self.recipes_endpoint,
            content_type='application/json',
            data=self.json_data
        )
        response = self.client.patch(
            self.recipes_detail_endpoint,
            content_type='application/json',
            data=self.json_changed_data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_author_cant_patch(self):
        self.authorize_user(self.token)
        self.client.post(
            self.recipes_endpoint,
            content_type='application/json',
            data=self.json_data
        )
        self.unauthorize_user()
        self.authorize_user(self.another_token)
        response = self.client.patch(
            self.recipes_detail_endpoint,
            content_type='application/json',
            data=self.json_changed_data
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_validation_for_patch(self):
        self.authorize_user(self.token)
        self.client.post(
            self.recipes_endpoint,
            content_type='application/json',
            data=self.json_data
        )
        response = self.client.patch(
            self.recipes_detail_endpoint,
            content_type='application/json',
            data={}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)






