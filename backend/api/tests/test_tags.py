import json

from rest_framework import status
from rest_framework.test import APITransactionTestCase

from api.models import Tag


class TagsAPITests(APITransactionTestCase):
    reset_sequences = True

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.tags_endpoint = '/api/tags/'
        cls.test_tag_url = cls.tags_endpoint + '1/'
        cls.not_existing_tag = cls.tags_endpoint + '2/'

        cls.empty_tags_list = []

        cls.test_tag = {
                "name": "Завтрак",
                "color": "#E26C2D",
                "slug": "breakfast"
              }

        cls.not_empty_tags_list = [
              {
                "id": 1,
                "name": "Завтрак",
                "color": "#E26C2D",
                "slug": "breakfast"
              }
        ]

        cls.tag_breakfast_data = cls.not_empty_tags_list[0]

    def create_tag(self):
        Tag.objects.create(
            name=self.test_tag['name'],
            color=self.test_tag['color'],
            slug=self.test_tag['slug']
        )

    def test_empty_tags_list(self):
        response = self.client.get(self.tags_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.empty_tags_list
        )

    def test_not_empty_tags_list(self):
        self.create_tag()
        response = self.client.get(self.tags_endpoint)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.not_empty_tags_list
        )

    def test_get_test_tag(self):
        self.create_tag()
        response = self.client.get(self.test_tag_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            self.tag_breakfast_data
        )

    def test_not_existing_tag_returns_404(self):
        response = self.client.get(self.not_existing_tag)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



