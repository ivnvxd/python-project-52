from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from task_manager.statuses.models import Status
from .testcase import StatusTestCase


class TestCreateStatus(StatusTestCase):
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

    def test_delete_bound_status(self) -> None:
        response = self.client.post(
            reverse_lazy('status_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('statuses'))
        self.assertEqual(Status.objects.count(), self.count)
