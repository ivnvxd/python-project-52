from django.test import TestCase
from django.urls import reverse


class AppTest(TestCase):

    def test_index_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
