from django.test import TestCase, Client, modify_settings
from django.urls import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist

from task_manager.tasks.models import Task
from task_manager.users.models import User


remove_rollbar = modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})


@remove_rollbar
class TaskTestCase(TestCase):
    fixtures = ['user.json', 'status.json', 'task.json', 'label.json']

    def setUp(self) -> None:
        self.client = Client()

        self.task1 = Task.objects.get(pk=1)
        self.count = Task.objects.count()

        self.user1 = User.objects.get(pk=1)
        self.client.force_login(self.user1)


class TestDeleteTask(TaskTestCase):
    def test_delete_task_view(self) -> None:
        response = self.client.get(
            reverse_lazy('task_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='tasks/delete.html')

    def test_delete_task_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(
            reverse_lazy('task_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))

    def test_delete_task_unauthorised_view(self) -> None:
        response = self.client.get(
            reverse_lazy('task_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))

    def test_delete_task(self) -> None:
        response = self.client.post(
            reverse_lazy('task_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))
        self.assertEqual(Task.objects.count(), self.count - 1)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(id=self.task1.id)

    def test_delete_task_not_logged_in(self) -> None:
        self.client.logout()

        response = self.client.post(
            reverse_lazy('task_delete', kwargs={'pk': 1})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
        self.assertEqual(Task.objects.count(), self.count)

    def test_delete_task_unauthorised(self) -> None:
        response = self.client.post(
            reverse_lazy('task_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('tasks'))
        self.assertEqual(Task.objects.count(), self.count)
