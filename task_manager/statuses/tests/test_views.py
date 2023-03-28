from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext as _
from task_manager.statuses.models import Status

User = get_user_model()

MSG_NO_PERMISSION = _('You are not authorized! Please sign in.')


class StatusListViewTest(TestCase):
    """Test case for the StatusListView."""

    fixtures = ['statuses.json', 'users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(User.objects.get(pk=1))

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/statuses/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'statuses/status_list.html')

    def test_list_all_statuses(self) -> None:
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['statuses']), 3)

    def test_view_has_links_to_change_and_delete(self) -> None:
        response = self.client.get(reverse('status_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        for status_id in range(1, len(response.context['statuses']) + 1):
            self.assertContains(response, f'/statuses/{status_id}/update/')
            self.assertContains(response, f'/statuses/{status_id}/delete/')

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()
        response = self.client.get(reverse('status_list'), follow=True)
        self.assertRedirects(response, reverse('login'))

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')


class StatusCreateViewTest(TestCase):
    """"Test case for StatusCreateView."""

    fixtures = ['users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(User.objects.get(pk=1))
        self.valid_data = {'name': 'status'}
        self.invalid_data = {'name': ''}

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/statuses/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('status_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'statuses/status_create.html')

    def test_create_status_with_valid_data(self) -> None:
        response = self.client.post(
            reverse('status_create'),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('status_list'))

        status = Status.objects.get(pk=1)
        self.assertEqual(status.name, self.valid_data['name'])
        self.assertTrue(status.created_at)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('The status successfully created'))
        self.assertEqual(message.tags, 'success')

    def test_do_not_create_status_with_invalid_data(self) -> None:
        response = self.client.post(
            reverse('status_create'),
            self.invalid_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(Status.objects.all())

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()
        response = self.client.get(reverse('status_create'), follow=True)
        self.assertRedirects(response, reverse('login'))

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')


class StatusUpdateViewTest(TestCase):
    """"Test case for StatusUpdateView."""

    fixtures = ['statuses.json', 'users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(User.objects.get(pk=1))
        self.valid_data = {'name': 'status'}
        self.invalid_data = {'name': ''}

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/statuses/1/update/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('status_update', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('status_update', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'statuses/status_create.html')

    def test_update_status_with_valid_data(self) -> None:
        response = self.client.post(
            reverse('status_update', args=[1]),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('status_list'))

        status = Status.objects.get(pk=1)
        self.assertEqual(status.name, self.valid_data['name'])
        self.assertTrue(status.created_at)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('The status successfully updated'))
        self.assertEqual(message.tags, 'success')

    def test_do_not_update_status_with_invalid_data(self) -> None:
        status_before = Status.objects.get(pk=1)
        response = self.client.post(
            reverse('status_update', args=[1]),
            self.invalid_data
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        status_after = Status.objects.get(pk=1)
        self.assertEqual(status_before, status_after)

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()
        response = self.client.get(
            reverse('status_update', args=[1]),
            follow=True
        )
        self.assertRedirects(response, reverse('login'))

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')


class StatusDeleteViewTest(TestCase):
    """"Test case for StatusDeleteView."""

    fixtures = ['labels.json', 'statuses.json', 'tasks.json', 'users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(User.objects.get(pk=1))

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/statuses/1/delete/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('status_delete', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('status_delete', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'statuses/status_delete.html')

    def test_delete_status(self) -> None:
        length_of_status_list_before = len(Status.objects.all())

        response = self.client.post(
            reverse('status_delete', args=[1]),
            follow=True
        )
        self.assertRedirects(response, reverse('status_list'))

        length_of_status_list_after = len(Status.objects.all())
        self.assertTrue(
            length_of_status_list_after == length_of_status_list_before - 1
        )
        with self.assertRaises(ObjectDoesNotExist):
            Status.objects.get(pk=1)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('The status successfully deleted'))
        self.assertEqual(message.tags, 'success')

    def test_do_not_delete_status_linked_to_task(self) -> None:
        status_before = Status.objects.get(pk=3)

        response = self.client.post(
            reverse('status_delete', args=[3]),
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('status_list'))

        status_after = Status.objects.get(pk=3)
        self.assertEqual(status_before, status_after)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message,
            _("Can't delete status because it's in use")
        )
        self.assertEqual(message.tags, 'error')

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()
        response = self.client.get(
            reverse('status_delete', args=[1]),
            follow=True
        )
        self.assertRedirects(response, reverse('login'))

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')
