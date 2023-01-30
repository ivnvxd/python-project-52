from django.urls import reverse_lazy

from .testcase import TaskTestCase


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


class TestCreateTaskView(TaskTestCase):
    def test_create_task_view(self) -> None:
        response = self.client.get(reverse_lazy('task_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_create_task_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(reverse_lazy('task_create'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestUpdateTaskView(TaskTestCase):
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


class TestDeleteTaskView(TaskTestCase):
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
