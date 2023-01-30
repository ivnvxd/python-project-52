from django.test import TestCase, Client

from task_manager.helpers import load_data, test_english, remove_rollbar
from task_manager.tasks.models import Task
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


@test_english
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
        self.labels = Label.objects.filter(pk=2)

        self.client.force_login(self.user1)
