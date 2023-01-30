from django.test import TestCase, Client, modify_settings
from django.urls import reverse_lazy

from task_manager.helpers import load_data
from task_manager.tasks.models import Task
from task_manager.users.models import User


remove_rollbar = modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})


@remove_rollbar
class TaskTestCase(TestCase):
    fixtures = ['user.json', 'status.json', 'task.json', 'label.json']
    test_task = load_data('test_task.json')

    def setUp(self) -> None:
        self.client = Client()

        self.task2 = Task.objects.get(pk=2)
        self.count = Task.objects.count()

        self.user1 = User.objects.get(pk=1)
        self.client.force_login(self.user1)


class TestUpdateTask(TaskTestCase):
    def test_update_task_view(self) -> None:
        response = self.client.get(
            reverse_lazy('task_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_update_task_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(
            reverse_lazy('task_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_update_task(self) -> None:
        task_data = self.test_task['update'].copy()
        response = self.client.post(
            reverse_lazy('task_update', kwargs={'pk': 2}),
            data=task_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))

        self.assertEqual(Task.objects.count(), self.count)
        self.assertEqual(
            Task.objects.get(id=self.task2.id).name,
            task_data['name']
        )
        self.assertEqual(
            Task.objects.get(id=self.task2.id).executor.id,
            task_data['executor']
        )

    def test_update_task_not_logged_in(self) -> None:
        self.client.logout()

        task_data = self.test_task['update'].copy()
        response = self.client.post(
            reverse_lazy('task_update', kwargs={'pk': 2}),
            data=task_data
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

        self.assertEqual(Task.objects.count(), self.count)
        self.assertNotEqual(
            Task.objects.get(id=self.task2.id).name,
            task_data['name']
        )
