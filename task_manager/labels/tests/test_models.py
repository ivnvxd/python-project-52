from django.utils import timezone

from task_manager.labels.models import Label
from .testcase import LabelTestCase


class LabelModelTest(LabelTestCase):
    def test_label_creation(self) -> None:
        label_data = self.test_label['create']['valid'].copy()

        label = Label.objects.create(
            name=label_data['name'],
            date_created=timezone.now()
        )

        self.assertTrue(isinstance(label, Label))
        self.assertEqual(label.__str__(), label_data['name'])
        self.assertEqual(label.name, label_data['name'])
