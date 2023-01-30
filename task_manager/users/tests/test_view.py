from django.urls import reverse_lazy

from .testcase import UserTestCase


class TestListUsers(UserTestCase):
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


class TestCreateUserView(UserTestCase):
    def test_sign_up_view(self) -> None:
        response = self.client.get(reverse_lazy('sign_up'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')


class TestUpdateUserView(UserTestCase):
    def test_update_self_view(self) -> None:
        self.client.force_login(self.user2)

        response = self.client.get(
            reverse_lazy('user_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_update_not_logged_in_view(self) -> None:
        response = self.client.get(
            reverse_lazy('user_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_update_other_view(self) -> None:
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse_lazy('user_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users'))


class TestDeleteUserView(UserTestCase):
    def test_delete_self_view(self) -> None:
        self.client.force_login(self.user3)

        response = self.client.get(
            reverse_lazy('user_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='users/delete.html')

    def test_delete_not_logged_in_view(self) -> None:
        response = self.client.get(
            reverse_lazy('user_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_delete_other_view(self) -> None:
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse_lazy('user_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('users'))
