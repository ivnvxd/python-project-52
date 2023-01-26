from django.test import TestCase
from django.test import Client
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from task_manager.helpers import load_data
from .models import Status
from task_manager.users.models import User


class StatusTestCase(TestCase):
    fixtures = ['user.json', 'status.json']
    test_status = load_data('test_status.json')

    def setUp(self) -> None:
        self.client = Client()

        self.status1 = Status.objects.get(pk=1)
        self.status2 = Status.objects.get(pk=2)
        self.status3 = Status.objects.get(pk=3)
        self.statuses = Status.objects.all()
        self.count = Status.objects.count()

        self.user1 = User.objects.get(pk=1)
        self.client.force_login(self.user1)


class TestReadStatus(StatusTestCase):
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


class TestCreateStatus(StatusTestCase):
    def test_create_status_view(self) -> None:
        response = self.client.get(reverse_lazy('status_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_create_status_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(reverse_lazy('status_create'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_create_valid_status(self) -> None:
        status_data = self.test_status['create']['valid'].copy()
        response = self.client.post(
            reverse_lazy('status_create'),
            data=status_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('statuses'))

        self.assertEqual(Status.objects.count(), self.count + 1)
        self.assertEqual(
            Status.objects.last().name,
            status_data['name']
        )

    def test_create_fields_missing(self) -> None:
        status_data = self.test_status['create']['missing_fields'].copy()
        response = self.client.post(
            reverse_lazy('status_create'),
            data=status_data
        )
        errors = response.context['form'].errors
        error_help = _('This field is required.')

        self.assertIn('name', errors)
        self.assertEqual(
            [error_help],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), self.count)

    def test_create_status_exists(self) -> None:
        status_data = self.test_status['create']['exists'].copy()
        response = self.client.post(
            reverse_lazy('status_create'),
            data=status_data
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Status with this Name already exists.')],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), self.count)

    def test_create_long_field(self) -> None:
        status_data = self.test_status['create']['valid'].copy()
        status_data.update({'name': 'name' * 50})

        response = self.client.post(
            reverse_lazy('status_create'),
            data=status_data
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Ensure this value has at most 150 characters '
               f'(it has {len(status_data["name"])}).')],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Status.objects.count(), self.count)


class TestUpdateStatus(StatusTestCase):
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

    def test_update_status(self) -> None:
        status_data = self.test_status['update'].copy()
        response = self.client.post(
            reverse_lazy('status_update', kwargs={'pk': 2}),
            data=status_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('statuses'))

        self.assertEqual(Status.objects.count(), self.count)
        self.assertEqual(
            Status.objects.get(id=self.status2.id).name,
            status_data['name']
        )

    def test_update_status_not_logged_in(self) -> None:
        self.client.logout()

        status_data = self.test_status['update'].copy()
        response = self.client.post(
            reverse_lazy('status_update', kwargs={'pk': 2}),
            data=status_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(Status.objects.count(), self.count)
        self.assertNotEqual(
            Status.objects.get(id=self.status2.id).name,
            status_data['name']
        )


class TestDeleteStatus(StatusTestCase):
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

    def test_delete_status(self) -> None:
        response = self.client.post(
            reverse_lazy('status_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('statuses'))
        self.assertEqual(Status.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(id=self.status3.id)

    def test_delete_status_not_logged_in(self) -> None:
        self.client.logout()

        response = self.client.post(
            reverse_lazy('status_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertEqual(Status.objects.count(), self.count)

    # TODO: add this test after adding tasks
    def test_delete_bound_status(self) -> None:
        pass
