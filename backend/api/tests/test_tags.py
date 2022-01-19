import json

from rest_framework import status
from rest_framework.test import APITestCase

from api.models import Tag


class TagsAPITests(APITestCase):

    tags_endpoint = '/api/tags/'
    test_tag_url = tags_endpoint + '1/'
    not_existing_tag = tags_endpoint + '2/'

    empty_tags_list = []

    test_tag = {
            "name": "Завтрак",
            "color": "#E26C2D",
            "slug": "breakfast"
          }

    not_empty_tags_list = [
          {
            "id": 1,
            "name": "Завтрак",
            "color": "#E26C2D",
            "slug": "breakfast"
          }
    ]

    tag_breakfast_data = not_empty_tags_list[0]

    def test_tags(self):

        response = self.client.get(self.tags_endpoint)
        with self.subTest(test='empty tags list'):
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )
            self.assertEqual(
                json.loads(response.content),
                self.empty_tags_list
            )

        Tag.objects.create(
            name=self.test_tag['name'],
            color=self.test_tag['color'],
            slug=self.test_tag['slug']
        )

        response = self.client.get(self.tags_endpoint)
        with self.subTest(test='not empty tags list'):
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )
            self.assertEqual(
                json.loads(response.content),
                self.not_empty_tags_list
            )

        response = self.client.get(self.test_tag_url)
        with self.subTest(test='get test tag'):
            self.assertEqual(
                response.status_code,
                status.HTTP_200_OK
            )
            self.assertEqual(
                json.loads(response.content),
                self.tag_breakfast_data
            )

        response = self.client.get(self.not_existing_tag)
        with self.subTest(test='not existing tag returns 404'):
            self.assertEqual(
                response.status_code,
                status.HTTP_404_NOT_FOUND
            )



