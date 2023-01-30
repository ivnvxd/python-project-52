from django.test import TestCase, Client

from task_manager.helpers import load_data, test_english, remove_rollbar
from task_manager.labels.models import Label
from task_manager.users.models import User


@test_english
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
