from django.test import TestCase, Client, modify_settings
from django.urls import reverse_lazy

from task_manager.tasks.models import Task
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


remove_rollbar = modify_settings(MIDDLEWARE={'remove': [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
]})


@remove_rollbar
class TaskTestCase(TestCase):
    fixtures = ['user.json', 'status.json', 'task.json', 'label.json']

    def setUp(self) -> None:
        self.client = Client()

        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.task3 = Task.objects.get(pk=3)

        self.tasks = Task.objects.all()
        self.count = Task.objects.count()

        self.user1 = User.objects.get(pk=1)
        self.status1 = Status.objects.get(pk=1)
        self.label2 = Label.objects.get(pk=2)

        self.client.force_login(self.user1)


class TestListTasks(TaskTestCase):
    def test_tasks_view(self) -> None:
        response = self.client.get(reverse_lazy('tasks'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='tasks/tasks.html'
        )

    def test_tasks_content(self) -> None:
        response = self.client.get(reverse_lazy('tasks'))

        self.assertEqual(len(response.context['tasks']), self.count)
        self.assertQuerysetEqual(
            response.context['tasks'],
            self.tasks,
            ordered=False
        )

    def test_tasks_links(self) -> None:
        response = self.client.get(reverse_lazy('tasks'))

        self.assertContains(response, '/tasks/create/')

        for pk in range(1, self.count + 1):
            self.assertContains(response, f'/tasks/{pk}/update/')
            self.assertContains(response, f'/tasks/{pk}/delete/')

    def test_tasks_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(reverse_lazy('tasks'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestFilterTasks(TaskTestCase):
    def test_filter_tasks_by_status(self) -> None:
        response = self.client.get(
            reverse_lazy('tasks'),
            {'status': self.status1.pk}
        )

        self.assertEqual(response.context['tasks'].count(), 2)
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)

    def test_filter_tasks_by_executor(self) -> None:
        response = self.client.get(
            reverse_lazy('tasks'),
            {'executor': self.user1.pk}
        )

        self.assertEqual(response.context['tasks'].count(), 2)
        self.assertNotContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)

    def test_filter_tasks_by_label(self) -> None:
        response = self.client.get(
            reverse_lazy('tasks'),
            {'labels': self.label2.pk}
        )

        self.assertEqual(response.context['tasks'].count(), 1)
        self.assertNotContains(response, self.task1.name)
        self.assertNotContains(response, self.task2.name)
        self.assertContains(response, self.task3.name)

    def test_filter_tasks_by_own_tasks(self) -> None:
        response = self.client.get(
            reverse_lazy('tasks'),
            {'own_tasks': 'on'}
        )

        self.assertEqual(response.context['tasks'].count(), 2)
        self.assertContains(response, self.task1.name)
        self.assertContains(response, self.task2.name)
        self.assertNotContains(response, self.task3.name)


class TestDetailedTask(TaskTestCase):
    def test_detailed_task_view(self) -> None:
        response = self.client.get(
            reverse_lazy('task_show', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='tasks/task_show.html'
        )

    def test_detailed_task_content(self) -> None:
        response = self.client.get(
            reverse_lazy('task_show', kwargs={'pk': 3})
        )

        labels = self.task3.labels.all()

        self.assertContains(response, '/tasks/3/update/')
        self.assertContains(response, '/tasks/3/delete/')

        self.assertContains(response, self.task3.name)
        self.assertContains(response, self.task3.description)
        self.assertContains(response, self.task3.author)
        self.assertContains(response, self.task3.executor)
        self.assertContains(response, self.task3.status)

        for label in labels:
            self.assertContains(response, label.name)

    def test_detailed_task_not_logged_in(self) -> None:
        self.client.logout()

        response = self.client.get(
            reverse_lazy('task_show', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
