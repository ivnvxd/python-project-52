from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

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

    def test_create_valid_user(self) -> None:
        self.client.logout()

        user_data = self.test_user['create']['valid'].copy()
        response = self.client.post(reverse_lazy('sign_up'), data=user_data)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(User.objects.count(), self.count + 1)
        self.assertEqual(
            User.objects.last().username,
            user_data['username']
        )

    def test_create_fields_missing(self) -> None:
        self.client.logout()

        user_data = self.test_user['create']['missing_fields'].copy()
        response = self.client.post(reverse_lazy('sign_up'), data=user_data)
        errors = response.context['form'].errors
        error_help = _('This field is required.')

        self.assertIn('username', errors)
        self.assertEqual(
            [error_help],
            errors['username']
        )

        self.assertIn('first_name', errors)
        self.assertEqual(
            [error_help],
            errors['first_name']
        )

        self.assertIn('last_name', errors)
        self.assertEqual(
            [error_help],
            errors['last_name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_invalid_username(self) -> None:
        self.client.logout()

        user_data = self.test_user['create']['invalid'].copy()
        response = self.client.post(reverse_lazy('sign_up'), data=user_data)
        errors = response.context['form'].errors

        self.assertIn('username', errors)
        self.assertEqual(
            [_('Enter a valid username. This value may contain only '
               'letters, numbers, and @/./+/-/_ characters.')],
            errors['username']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_username_exists(self) -> None:
        self.client.logout()

        user_data = self.test_user['create']['exists'].copy()
        response = self.client.post(reverse_lazy('sign_up'), data=user_data)
        errors = response.context['form'].errors

        self.assertIn('username', errors)
        self.assertEqual(
            [_('A user with that username already exists.')],
            errors['username']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_long_fields(self) -> None:
        self.client.logout()

        user_data = self.test_user['create']['valid'].copy()
        user_data.update({'username': 'username' * 20})
        user_data.update({'first_name': 'firstname' * 20})
        user_data.update({'last_name': 'lastname' * 20})

        response = self.client.post(reverse_lazy('sign_up'), data=user_data)
        errors = response.context['form'].errors

        self.assertIn('username', errors)
        self.assertEqual(
            [_('Ensure this value has at most 150 characters '
               f'(it has {len(user_data["username"])}).')],
            errors['username']
        )

        self.assertIn('first_name', errors)
        self.assertEqual(
            [_('Ensure this value has at most 150 characters '
               f'(it has {len(user_data["first_name"])}).')],
            errors['first_name']
        )

        self.assertIn('last_name', errors)
        self.assertEqual(
            [_('Ensure this value has at most 150 characters '
               f'(it has {len(user_data["last_name"])}).')],
            errors['last_name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_password_missing(self) -> None:
        self.client.logout()

        user_data = self.test_user['create']['pass_missing'].copy()
        response = self.client.post(reverse_lazy('sign_up'), data=user_data)
        errors = response.context['form'].errors
        error_help = _('This field is required.')

        self.assertIn('password1', errors)
        self.assertEqual(
            [error_help],
            errors['password1']
        )

        self.assertIn('password2', errors)
        self.assertEqual(
            [error_help],
            errors['password2']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_password_dont_match(self) -> None:
        self.client.logout()

        user_data = self.test_user['create']['pass_not_match'].copy()
        response = self.client.post(reverse_lazy('sign_up'), data=user_data)
        errors = response.context['form'].errors

        self.assertIn('password2', errors)
        self.assertEqual(
            [_('The two password fields didn’t match.')],
            errors['password2']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)

    def test_create_password_too_short(self) -> None:
        self.client.logout()

        user_data = self.test_user['create']['pass_too_short'].copy()
        response = self.client.post(reverse_lazy('sign_up'), data=user_data)
        errors = response.context['form'].errors

        self.assertIn('password2', errors)
        self.assertEqual(
            [_('This password is too short. '
               'It must contain at least 3 characters.')],
            errors['password2']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(User.objects.count(), self.count)


class TestUpdateUser(UserTestCase):
    def test_update_view(self) -> None:
        response = self.client.get(
            reverse_lazy('user_update', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/form.html')


class TestDeleteUser(UserTestCase):
    def test_delete_view(self) -> None:
        response = self.client.get(
            reverse_lazy('user_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/delete.html')
