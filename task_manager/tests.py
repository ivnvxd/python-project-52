from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class HomePageTestCase(TestCase):

    def test_index_view(self) -> None:
        response = self.client.get(reverse_lazy('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='index.html')
        self.assertContains(response, _('Hello, World!'), status_code=200)
