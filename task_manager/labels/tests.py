from django.test import TestCase, Client, modify_settings, override_settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from task_manager.helpers import load_data
from .models import Label
from task_manager.users.models import User


english = override_settings(
    LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),),
)
remove_rollbar = modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})


@english
@remove_rollbar
class LabelTestCase(TestCase):
    fixtures = ['user.json', 'status.json', 'task.json', 'label.json']
    test_label = load_data('test_label.json')

    def setUp(self) -> None:
        self.client = Client()

        self.label1 = Label.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)
        self.label3 = Label.objects.get(pk=3)
        self.labels = Label.objects.all()
        self.count = Label.objects.count()

        self.user1 = User.objects.get(pk=1)

        self.client.force_login(self.user1)


class TestListLabels(LabelTestCase):
    def test_labels_view(self) -> None:
        response = self.client.get(reverse_lazy('labels'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='labels/labels.html'
        )

    def test_labels_content(self) -> None:
        response = self.client.get(reverse_lazy('labels'))

        self.assertEqual(len(response.context['labels']), self.count)
        self.assertQuerysetEqual(
            response.context['labels'],
            self.labels,
            ordered=False
        )

    def test_labels_links(self) -> None:
        response = self.client.get(reverse_lazy('labels'))

        self.assertContains(response, '/labels/create/')

        for pk in range(1, self.count + 1):
            self.assertContains(response, f'/labels/{pk}/update/')
            self.assertContains(response, f'/labels/{pk}/delete/')

    def test_labels_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(reverse_lazy('labels'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestCreateLabel(LabelTestCase):
    def test_create_label_view(self) -> None:
        response = self.client.get(reverse_lazy('label_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_create_label_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(reverse_lazy('label_create'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_create_valid_label(self) -> None:
        label_data = self.test_label['create']['valid'].copy()
        response = self.client.post(
            reverse_lazy('label_create'),
            data=label_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels'))

        self.assertEqual(Label.objects.count(), self.count + 1)
        self.assertEqual(
            Label.objects.last().name,
            label_data['name']
        )

    def test_create_fields_missing(self) -> None:
        label_data = self.test_label['create']['missing_fields'].copy()
        response = self.client.post(
            reverse_lazy('label_create'),
            data=label_data
        )
        errors = response.context['form'].errors
        error_help = _('This field is required.')

        self.assertIn('name', errors)
        self.assertEqual(
            [error_help],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), self.count)

    def test_create_label_exists(self) -> None:
        label_data = self.test_label['create']['exists'].copy()
        response = self.client.post(
            reverse_lazy('label_create'),
            data=label_data
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Label with this Name already exists.')],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), self.count)

    def test_create_long_field(self) -> None:
        label_data = self.test_label['create']['valid'].copy()
        label_data.update({'name': 'name' * 50})

        response = self.client.post(
            reverse_lazy('label_create'),
            data=label_data
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Ensure this value has at most 150 characters '
               f'(it has {len(label_data["name"])}).')],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Label.objects.count(), self.count)


class TestUpdateLabel(LabelTestCase):
    def test_update_label_view(self) -> None:
        response = self.client.get(
            reverse_lazy('label_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_update_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(
            reverse_lazy('label_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_update_label(self) -> None:
        label_data = self.test_label['update'].copy()
        response = self.client.post(
            reverse_lazy('label_update', kwargs={'pk': 2}),
            data=label_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels'))

        self.assertEqual(Label.objects.count(), self.count)
        self.assertEqual(
            Label.objects.get(id=self.label2.id).name,
            label_data['name']
        )

    def test_update_label_not_logged_in(self) -> None:
        self.client.logout()

        label_data = self.test_label['update'].copy()
        response = self.client.post(
            reverse_lazy('label_update', kwargs={'pk': 2}),
            data=label_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(Label.objects.count(), self.count)
        self.assertNotEqual(
            Label.objects.get(id=self.label2.id).name,
            label_data['name']
        )


class TestDeleteLabel(LabelTestCase):
    def test_delete_label_view(self) -> None:
        response = self.client.get(
            reverse_lazy('label_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/delete.html')

    def test_delete_label_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(
            reverse_lazy('label_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_delete_label(self) -> None:
        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels'))
        self.assertEqual(Label.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(id=self.label3.id)

    def test_delete_label_not_logged_in(self) -> None:
        self.client.logout()

        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertEqual(Label.objects.count(), self.count)

    def test_delete_bound_label(self) -> None:
        response = self.client.post(
            reverse_lazy('label_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('labels'))
        self.assertEqual(Label.objects.count(), self.count)
