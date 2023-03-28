from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext as _
from task_manager.labels.models import Label

User = get_user_model()

MSG_NO_PERMISSION = _('You are not authorized! Please sign in.')


class LabelsListViewTest(TestCase):
    """Test case for the LabelsListView."""

    fixtures = ['labels.json', 'users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(User.objects.get(pk=1))

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/labels/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'labels/label_list.html')

    def test_list_all_labels(self) -> None:
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['labels']), 3)

    def test_view_has_links_to_change_and_delete(self) -> None:
        response = self.client.get(reverse('label_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        for label_id in range(1, len(response.context['labels']) + 1):
            self.assertContains(response, f'/labels/{label_id}/update/')
            self.assertContains(response, f'/labels/{label_id}/delete/')

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()
        response = self.client.get(reverse('label_list'), follow=True)
        self.assertRedirects(response, reverse('login'))

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')


class LabelCreateViewTest(TestCase):
    """"Test case for LabelCreateView."""

    fixtures = ['users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(User.objects.get(pk=1))
        self.valid_data = {'name': 'label'}
        self.invalid_data = {'name': ''}

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/labels/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('label_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'labels/label_create.html')

    def test_create_label_with_valid_data(self) -> None:
        response = self.client.post(
            reverse('label_create'),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('label_list'))

        label = Label.objects.get(pk=1)
        self.assertEqual(label.name, self.valid_data['name'])
        self.assertTrue(label.created_at)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('The label successfully created'))
        self.assertEqual(message.tags, 'success')

    def test_do_not_create_label_with_invalid_data(self) -> None:
        response = self.client.post(
            reverse('label_create'),
            self.invalid_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(Label.objects.all())

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()
        response = self.client.get(reverse('label_create'), follow=True)
        self.assertRedirects(response, reverse('login'))

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')


class LabelUpdateViewTest(TestCase):
    """"Test case for LabelUpdateView."""

    fixtures = ['labels.json', 'users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(User.objects.get(pk=1))
        self.valid_data = {'name': 'status'}
        self.invalid_data = {'name': ''}

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/labels/1/update/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('label_update', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('label_update', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'labels/label_create.html')

    def test_update_label_with_valid_data(self) -> None:
        response = self.client.post(
            reverse('label_update', args=[1]),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('label_list'))

        label = Label.objects.get(pk=1)
        self.assertEqual(label.name, self.valid_data['name'])
        self.assertTrue(label.created_at)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('The label successfully updated'))
        self.assertEqual(message.tags, 'success')

    def test_do_not_update_label_with_invalid_data(self) -> None:
        label_before = Label.objects.get(pk=1)
        response = self.client.post(
            reverse('label_update', args=[1]),
            self.invalid_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        label_after = Label.objects.get(pk=1)
        self.assertEqual(label_before, label_after)

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()
        response = self.client.get(
            reverse('label_update', args=[1]),
            follow=True
        )
        self.assertRedirects(response, reverse('login'))

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')


class LabelDeleteViewTest(TestCase):
    """"Test case for LabelDeleteView."""

    fixtures = ['labels.json', 'statuses.json', 'tasks.json', 'users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(User.objects.get(pk=1))

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/labels/1/delete/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('label_delete', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('label_delete', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'labels/label_delete.html')

    def test_delete_label(self) -> None:
        length_of_label_list_before = len(Label.objects.all())

        response = self.client.post(
            reverse('label_delete', args=[1]),
            follow=True
        )
        self.assertRedirects(response, reverse('label_list'))

        length_of_label_list_after = len(Label.objects.all())
        self.assertTrue(
            length_of_label_list_after == length_of_label_list_before - 1
        )
        with self.assertRaises(ObjectDoesNotExist):
            Label.objects.get(pk=1)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('The label successfully deleted'))
        self.assertEqual(message.tags, 'success')

    def test_do_not_delete_label_linked_to_task(self) -> None:
        label_before = Label.objects.get(pk=3)

        response = self.client.post(
            reverse('label_delete', args=[3]),
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('label_list'))

        label_after = Label.objects.get(pk=3)
        self.assertEqual(label_before, label_after)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message,
            _("Can't delete label because it's in use")
        )
        self.assertEqual(message.tags, 'error')

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()
        response = self.client.get(
            reverse('label_delete', args=[1]),
            follow=True
        )
        self.assertRedirects(response, reverse('login'))

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')
