import json

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Ingredient


class TagsAPITests(APITestCase):

    ingredients_endpoint = '/api/ingredients/'
    test_ingredient_url = ingredients_endpoint + '1/'
    not_existing_ingredient = ingredients_endpoint + '2/'

    empty_ingredients_list = []

    test_ingredient = {
            "name": "Капуста",
            "measurement_unit": "кг"
          }

    not_empty_ingredients_list = [
          {
            "id": 1,
            "name": "Капуста",
            "measurement_unit": "кг"
          }
    ]

    ingredient_data = not_empty_ingredients_list[0]
    search_str = ingredient_data['name'][0:2]

    search_url = ingredients_endpoint + f'?name={search_str}'
    search_url_not_exists = ingredients_endpoint + '?name=not_exists'

    def test_ingredients(self):

        response = self.client.get(self.ingredients_endpoint)
        with self.subTest(test='empty ingredients list'):
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )
            self.assertEqual(
                json.loads(response.content),
                self.empty_ingredients_list
            )

        Ingredient.objects.create(
            name=self.test_ingredient['name'],
            measurement_unit=self.test_ingredient['measurement_unit']
            )

        response = self.client.get(self.ingredients_endpoint)
        with self.subTest(test='not empty ingredients list'):
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )
            self.assertEqual(
                json.loads(response.content),
                self.not_empty_ingredients_list
            )

        response = self.client.get(self.test_ingredient_url)
        with self.subTest(test='get test ingredient'):
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )
            self.assertEqual(
                json.loads(response.content),
                self.ingredient_data
            )

        response = self.client.get(self.not_existing_ingredient)
        with self.subTest(test='not existing tag returns 404'):
            self.assertEqual(
                response.status_code,
                status.HTTP_404_NOT_FOUND
            )

        response = self.client.get(self.search_url)
        with self.subTest(test='searching kapusta'):
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )
            self.assertEqual(
                json.loads(response.content),
                self.not_empty_ingredients_list
            )

        response = self.client.get(self.search_url_not_exists)
        with self.subTest(test='searching not existing ingredient'):
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )
            self.assertEqual(
                json.loads(response.content),
                self.empty_ingredients_list
            )


