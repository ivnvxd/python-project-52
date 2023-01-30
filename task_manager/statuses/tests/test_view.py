from django.urls import reverse_lazy

from .testcase import StatusTestCase


class TestListStatuses(StatusTestCase):
    def test_statuses_view(self) -> None:
        response = self.client.get(reverse_lazy('statuses'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='statuses/statuses.html'
        )

    def test_statuses_content(self) -> None:
        response = self.client.get(reverse_lazy('statuses'))

        self.assertEqual(len(response.context['statuses']), self.count)
        self.assertQuerysetEqual(
            response.context['statuses'],
            self.statuses,
            ordered=False
        )

    def test_statuses_links(self) -> None:
        response = self.client.get(reverse_lazy('statuses'))

        self.assertContains(response, '/statuses/create/')

        for pk in range(1, self.count + 1):
            self.assertContains(response, f'/statuses/{pk}/update/')
            self.assertContains(response, f'/statuses/{pk}/delete/')

    def test_statuses_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(reverse_lazy('statuses'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestCreateStatusView(StatusTestCase):
    def test_create_status_view(self) -> None:
        response = self.client.get(reverse_lazy('status_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_create_status_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(reverse_lazy('status_create'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestUpdateStatusView(StatusTestCase):
    def test_update_status_view(self) -> None:
        response = self.client.get(
            reverse_lazy('status_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_update_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(
            reverse_lazy('status_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestDeleteStatusView(StatusTestCase):
    def test_delete_status_view(self) -> None:
        response = self.client.get(
            reverse_lazy('status_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='statuses/delete.html')

    def test_delete_status_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(
            reverse_lazy('status_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
