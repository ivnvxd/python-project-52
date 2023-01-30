from django.test import TestCase, Client, modify_settings, override_settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.helpers import load_data
from task_manager.tasks.models import Task
from task_manager.users.models import User


english = override_settings(
    LANGUAGE_CODE='en-US', LANGUAGES=(('en', 'English'),),
)
remove_rollbar = modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})


@english
@remove_rollbar
class TaskTestCase(TestCase):
    fixtures = ['user.json', 'status.json', 'task.json', 'label.json']
    test_task = load_data('test_task.json')

    def setUp(self) -> None:
        self.client = Client()

        self.count = Task.objects.count()

        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

        self.client.force_login(self.user1)


class TestCreateTask(TaskTestCase):
    def test_create_task_view(self) -> None:
        response = self.client.get(reverse_lazy('task_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_create_task_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(reverse_lazy('task_create'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_create_valid_task(self) -> None:
        task_data = self.test_task['create']['valid'].copy()
        response = self.client.post(
            reverse_lazy('task_create'),
            data=task_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))

        self.assertEqual(Task.objects.count(), self.count + 1)
        self.assertEqual(
            Task.objects.last().name,
            task_data['name']
        )
        self.assertEqual(
            Task.objects.last().author,
            self.user1
        )
        self.assertEqual(
            Task.objects.last().executor,
            self.user2
        )

    def test_create_fields_missing(self) -> None:
        task_data = self.test_task['create']['missing_fields'].copy()
        response = self.client.post(
            reverse_lazy('task_create'),
            data=task_data
        )
        errors = response.context['form'].errors
        error_help = _('This field is required.')

        self.assertIn('name', errors)
        self.assertEqual(
            [error_help],
            errors['name']
        )

        self.assertIn('executor', errors)
        self.assertEqual(
            [error_help],
            errors['executor']
        )

        self.assertIn('status', errors)
        self.assertEqual(
            [error_help],
            errors['status']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), self.count)

    def test_create_task_exists(self) -> None:
        task_data = self.test_task['create']['exists'].copy()
        response = self.client.post(
            reverse_lazy('task_create'),
            data=task_data
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Task with this Name already exists.')],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), self.count)

    def test_create_long_field(self) -> None:
        task_data = self.test_task['create']['valid'].copy()
        task_data.update({'name': 'name' * 50})

        response = self.client.post(
            reverse_lazy('task_create'),
            data=task_data
        )
        errors = response.context['form'].errors

        self.assertIn('name', errors)
        self.assertEqual(
            [_('Ensure this value has at most 150 characters '
               f'(it has {len(task_data["name"])}).')],
            errors['name']
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), self.count)
