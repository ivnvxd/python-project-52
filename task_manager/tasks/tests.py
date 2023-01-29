from django.test import TestCase, Client, modify_settings, override_settings
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ObjectDoesNotExist

from task_manager.helpers import load_data
from .models import Task
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


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

        self.task1 = Task.objects.get(pk=1)
        self.task2 = Task.objects.get(pk=2)
        self.task3 = Task.objects.get(pk=3)
        self.tasks = Task.objects.all()
        self.count = Task.objects.count()

        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

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


class TestUpdateTask(TaskTestCase):
    def test_update_task_view(self) -> None:
        response = self.client.get(
            reverse_lazy('task_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_update_not_logged_in_view(self) -> None:
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

    def test_update_status_not_logged_in(self) -> None:
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
