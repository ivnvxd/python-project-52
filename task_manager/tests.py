from django.test import TestCase
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.test import Client

from task_manager.users.models import User


class HomePageTestCase(TestCase):

    def test_index_view(self) -> None:
        response = self.client.get(reverse_lazy('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='index.html')
        self.assertContains(response, _('Hello, World!'), status_code=200)


class TestLoginUser(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.credentials = {
            'username': 'test_user',
            'password': 'te$t_pa$$word'
        }
        self.user = User.objects.create_user(**self.credentials)

    def test_user_login_view(self) -> None:
        response = self.client.get(reverse_lazy('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/form.html')

    def test_user_login(self) -> None:
        response = self.client.post(
            reverse_lazy('login'),
            self.credentials,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse_lazy('home'))
        self.assertTrue(response.context['user'].is_authenticated)
