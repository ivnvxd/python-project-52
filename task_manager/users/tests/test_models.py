from task_manager.users.models import User
from .testcase import UserTestCase


class UserModelTest(UserTestCase):
    def test_user_creation(self) -> None:
        user_data = self.test_user['create']['valid'].copy()
        full_name = user_data['first_name'] + ' ' + user_data['last_name']

        user = User.objects.create(
            username=user_data['username'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name']
        )

        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.__str__(), full_name)
        self.assertEqual(user.username, user_data['username'])
        self.assertEqual(user.first_name, user_data['first_name'])
        self.assertEqual(user.last_name, user_data['last_name'])
