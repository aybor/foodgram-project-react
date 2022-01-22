import json

from rest_framework import status
from rest_framework.test import APITransactionTestCase

from api.models import Ingredient


class TagsAPITests(APITransactionTestCase):
    reset_sequences = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ingredients_endpoint = '/api/ingredients/'
        cls.test_ingredient_url = cls.ingredients_endpoint + '1/'
        cls.not_existing_ingredient = cls.ingredients_endpoint + '2/'

        cls.empty_ingredients_list = []

        cls.test_ingredient = {
                "name": "Капуста",
                "measurement_unit": "кг"
              }

        cls.not_empty_ingredients_list = [
              {
                "id": 1,
                "name": "Капуста",
                "measurement_unit": "кг"
              }
        ]

        cls.ingredient_data = cls.not_empty_ingredients_list[0]
        cls.search_str = cls.ingredient_data['name'][0:2]

        cls.search_url = cls.ingredients_endpoint + f'?name={cls.search_str}'
        cls.search_url_not_exists = (
            cls.ingredients_endpoint
            + '?name=not_exists'
        )

    def create_ingredient(self):
        Ingredient.objects.create(
            name=self.test_ingredient['name'],
            measurement_unit=self.test_ingredient['measurement_unit']
        )

    def test_empty_ingredients_list(self):
        response = self.client.get(self.ingredients_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.empty_ingredients_list
        )

    def test_not_empty_ingredients_list(self):
        self.create_ingredient()
        response = self.client.get(self.ingredients_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.not_empty_ingredients_list
        )

    def test_get_ingredient(self):
        self.create_ingredient()
        response = self.client.get(self.test_ingredient_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.ingredient_data
        )

    def test_not_existing_tag_return_404(self):
        response = self.client.get(self.not_existing_ingredient)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_search_for_ingredient(self):
        self.create_ingredient()
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.not_empty_ingredients_list
        )

    def test_search_for_not_existing_ingredient(self):
        response = self.client.get(self.search_url_not_exists)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.empty_ingredients_list
        )
