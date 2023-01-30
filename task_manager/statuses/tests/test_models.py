from django.utils import timezone

from task_manager.statuses.models import Status
from .testcase import StatusTestCase


class StatusModelTest(StatusTestCase):
    def test_status_creation(self) -> None:
        status_data = self.test_status['create']['valid'].copy()

        status = Status.objects.create(
            name=status_data['name'],
            date_created=timezone.now()
        )

        self.assertTrue(isinstance(status, Status))
        self.assertEqual(status.__str__(), status_data['name'])
        self.assertEqual(status.name, status_data['name'])
