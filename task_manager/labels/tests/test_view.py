from django.urls import reverse_lazy

from .testcase import LabelTestCase


class TestListLabels(LabelTestCase):
    def test_labels_view(self) -> None:
        response = self.client.get(reverse_lazy('labels'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            template_name='labels/labels.html'
        )

    def test_labels_content(self) -> None:
        response = self.client.get(reverse_lazy('labels'))

        self.assertEqual(len(response.context['labels']), self.count)
        self.assertQuerysetEqual(
            response.context['labels'],
            self.labels,
            ordered=False
        )

    def test_labels_links(self) -> None:
        response = self.client.get(reverse_lazy('labels'))

        self.assertContains(response, '/labels/create/')

        for pk in range(1, self.count + 1):
            self.assertContains(response, f'/labels/{pk}/update/')
            self.assertContains(response, f'/labels/{pk}/delete/')

    def test_labels_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(reverse_lazy('labels'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestCreateLabelView(LabelTestCase):
    def test_create_label_view(self) -> None:
        response = self.client.get(reverse_lazy('label_create'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_create_label_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(reverse_lazy('label_create'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestUpdateLabelView(LabelTestCase):
    def test_update_label_view(self) -> None:
        response = self.client.get(
            reverse_lazy('label_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='form.html')

    def test_update_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(
            reverse_lazy('label_update', kwargs={'pk': 2})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))


class TestDeleteLabelView(LabelTestCase):
    def test_delete_label_view(self) -> None:
        response = self.client.get(
            reverse_lazy('label_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='labels/delete.html')

    def test_delete_label_not_logged_in_view(self) -> None:
        self.client.logout()

        response = self.client.get(
            reverse_lazy('label_delete', kwargs={'pk': 3})
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy('login'))
