from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy

from task_manager.helpers import load_data
from .models import User


class UserTestCase(TestCase):
    fixtures = ['user.json']
    test_user = load_data('test_user.json')

    def setUp(self) -> None:
        self.client = Client()

        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)
        self.users = User.objects.all()
        self.count = User.objects.count()


class TestReadUser(UserTestCase):

    def test_users_view(self) -> None:
        response = self.client.get(reverse_lazy('users'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/users.html')

    def test_users_content(self) -> None:
        response = self.client.get(reverse_lazy('users'))

        self.assertEqual(len(response.context['users']), self.count)
        self.assertQuerysetEqual(
            response.context['users'],
            self.users,
            ordered=False
        )

    def test_users_links(self) -> None:
        response = self.client.get(reverse_lazy('users'))

        self.assertContains(response, '/users/create/')

        for pk in range(1, self.count + 1):
            self.assertContains(response, f'/users/{pk}/update/')
            self.assertContains(response, f'/users/{pk}/delete/')


class TestCreateUser(UserTestCase):
    def test_sign_up_view(self) -> None:
        response = self.client.get(reverse_lazy('sign_up'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/form.html')

    def test_create_user(self) -> None:
        self.client.logout()

        user_data = self.test_user['valid']

        response = self.client.post(reverse_lazy('sign_up'), data=user_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(User.objects.count(), self.count + 1)
        self.assertEqual(
            User.objects.last().username,
            user_data['username']
        )


class TestUpdateUser(UserTestCase):
    def test_update_view(self) -> None:
        response = self.client.get(reverse_lazy('user_update', kwargs={'pk': 1}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/form.html')


class TestDeleteUser(UserTestCase):
    def test_delete_view(self) -> None:
        response = self.client.get(reverse_lazy('user_delete', kwargs={'pk': 3}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/delete.html')
