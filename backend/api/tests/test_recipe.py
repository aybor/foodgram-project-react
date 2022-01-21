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

        cls.user = User.objects.create_user(
            email='vpupkin@yandex.ru',
            username='vasya.pupkin',
            first_name='Вася',
            last_name='Пупкин',
            password='some_strong_psw'
        )

        cls.tag = Tag.objects.create(
            name='test_tag_name',
            color='#FFFFFF',
            slug='test_tag_slug'
        )

        cls.ingredient = Ingredient.objects.create(
            name='test_ingredient',
            measurement_unit='test'
        )

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

        cls.token = Token.objects.create(user=cls.user)

    def post_recipe(self, data):
        return self.client.post(
            self.recipes_endpoint,
            data=json.dumps(data),
            content_type='application/json'
        )

    def authorize_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION="Token " + str(self.token)
        )

    def unauthorize_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="")

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)


    def test_recipes_allow_for_any(self):
        response = self.client.get(self.recipes_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.empty_recipes_list
        )

    def test_create_recipe_not_allow_for_anonymous(self):
        response = self.post_recipe(self.test_recipe_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_recipe_not_allowed_for_anonymous(self):
        Recipe.objects.create(kwargs=self.test_recipe_data)
        response = self.client.get(self.recipes_detail_endpoint)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_recipe_allow_for_authorized(self):
        self.authorize_user()
        response = self.post_recipe(self.test_recipe_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_validation_for_recipes_create(self):
        self.authorize_user()
        response = self.post_recipe({})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_get_recipe_allowed_for_authorized(self):
        self.authorize_user()
        self.post_recipe(self.test_recipe_data)
        response = self.client.get(self.recipes_detail_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)



