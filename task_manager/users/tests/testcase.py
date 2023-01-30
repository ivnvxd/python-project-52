from django.test import TestCase, Client

from task_manager.helpers import load_data, test_english, remove_rollbar
from task_manager.users.models import User


@test_english
@remove_rollbar
class UserTestCase(TestCase):
    fixtures = ['user.json', 'status.json', 'task.json', 'label.json']
    test_user = load_data('test_user.json')

    def setUp(self) -> None:
        self.client = Client()

        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)

        self.users = User.objects.all()
        self.count = User.objects.count()
