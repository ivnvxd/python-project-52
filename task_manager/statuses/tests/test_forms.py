from task_manager.statuses.forms import StatusForm
from .testcase import StatusTestCase


class StatusFormTest(StatusTestCase):
    def test_valid_form(self) -> None:
        status_data = self.test_status['create']['valid'].copy()
        form = StatusForm(data=status_data)

        self.assertTrue(form.is_valid())

    def test_invalid_form(self) -> None:
        status_data = self.test_status['create']['missing_fields'].copy()
        form = StatusForm(data=status_data)

        self.assertFalse(form.is_valid())
