from django.utils import timezone

from task_manager.tasks.models import Task
from .testcase import TaskTestCase


class TaskModelTest(TaskTestCase):
    def test_task_creation(self) -> None:
        task_data = self.test_task['create']['valid'].copy()

        task = Task.objects.create(
            name=task_data['name'],
            description=task_data['description'],
            date_created=timezone.now(),
            author=self.user1,
            status=self.status1,
            executor=self.user2,
        )
        task.labels.set(self.labels)

        self.assertTrue(isinstance(task, Task))
        self.assertEqual(task.__str__(), task_data['name'])
        self.assertEqual(task.name, task_data['name'])
        self.assertEqual(task.description, task_data['description'])
        self.assertEqual(task.author, self.user1)
        self.assertEqual(task.status, self.status1)
        self.assertEqual(task.executor, self.user2)
        self.assertEqual(task.labels.get(pk=2), self.label2)
