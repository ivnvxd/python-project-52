from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.helpers import test_english, remove_rollbar
from task_manager.users.models import User


@test_english
@remove_rollbar
class HomeTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()

        self.credentials = {
            'username': 'test_user',
            'password': 'te$t_pa$$word'
        }
        self.user = User.objects.create_user(**self.credentials)


class HomePageTestCase(HomeTestCase):
    def test_index_view(self) -> None:
        response = self.client.get(reverse_lazy('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='index.html')
        self.assertContains(response, _('Task Manager'), status_code=200)

    def test_header_links_logged_in(self) -> None:
        self.client.force_login(self.user)
        response = self.client.get(reverse_lazy('home'))

        self.assertContains(response, '/users/')
        self.assertContains(response, '/statuses/')
        self.assertContains(response, '/labels/')
        self.assertContains(response, '/tasks/')
        self.assertContains(response, '/logout/')

        self.assertNotContains(response, '/login/')

    def test_header_links_not_logged_in(self) -> None:
        response = self.client.get(reverse_lazy('home'))

        self.assertContains(response, '/users/')
        self.assertContains(response, '/login/')

        self.assertNotContains(response, '/statuses/')
        self.assertNotContains(response, '/labels/')
        self.assertNotContains(response, '/tasks/')
        self.assertNotContains(response, '/logout/')


class TestLoginUser(HomeTestCase):
    def test_user_login_view(self) -> None:
        response = self.client.get(reverse_lazy('login'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_user_login(self) -> None:
        response = self.client.post(
            reverse_lazy('login'),
            self.credentials,
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse_lazy('home'))
        self.assertTrue(response.context['user'].is_authenticated)


class TestLogoutUser(HomeTestCase):
    def test_user_logout(self) -> None:
        self.client.force_login(self.user)

        response = self.client.post(
            reverse_lazy('logout'),
            follow=True
        )

        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse_lazy('home'))
        self.assertFalse(response.context['user'].is_authenticated)
