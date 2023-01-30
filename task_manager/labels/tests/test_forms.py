from task_manager.labels.forms import LabelForm
from .testcase import LabelTestCase


class LabelFormTest(LabelTestCase):
    def test_valid_form(self) -> None:
        label_data = self.test_label['create']['valid'].copy()
        form = LabelForm(data=label_data)

        self.assertTrue(form.is_valid())

    def test_invalid_form(self) -> None:
        label_data = self.test_label['create']['missing_fields'].copy()
        form = LabelForm(data=label_data)

        self.assertFalse(form.is_valid())
