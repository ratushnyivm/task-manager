from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.test.utils import ignore_warnings
from django.urls import reverse
from django.utils.translation import gettext as _
from task_manager.users.views import MSG_NO_PERMISSION

User = get_user_model()

ignore_warnings(message="No directory at", module="whitenoise.base").enable()


class UsersListViewTest(TestCase):
    """Test case for the UsersListView."""

    fixtures = ['users.json']

    def setUp(self) -> None:
        self.client = Client()

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/users_list.html')

    def test_list_all_users(self) -> None:
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['users']), 3)

    def test_view_has_links_to_change_and_delete(self) -> None:
        response = self.client.get(reverse('users_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        for user_id in range(1, len(response.context['users']) + 1):
            self.assertContains(response, f'/users/{user_id}/update/')
            self.assertContains(response, f'/users/{user_id}/delete/')


class UserCreateViewTest(TestCase):
    """"Test case for UserCreateView"""

    def setUp(self) -> None:
        self.client = Client()
        self.valid_data = {
            'username': 'user_10',
            'first_name': 'First_name_user_10',
            'last_name': 'Last_name_user_10',
            'password1': 'password_10',
            'password2': 'password_10',
        }

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/users/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('user_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/user_create.html')

    def test_create_user_with_valid_data(self) -> None:
        response = self.client.post(
            reverse('user_create'),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('login'))

        user = User.objects.get(pk=1)
        self.assertEqual(user.username, self.valid_data['username'])
        self.assertEqual(user.first_name, self.valid_data['first_name'])
        self.assertEqual(user.last_name, self.valid_data['last_name'])

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('User successfully registered'))
        self.assertEqual(message.tags, 'success')

    def test_do_not_create_user_without_username(self) -> None:
        invalid_data = self.valid_data
        invalid_data['username'] = ''

        response = self.client.post(
            reverse('user_create'),
            invalid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(User.objects.all())

    def test_do_not_create_user_without_first_name(self) -> None:
        invalid_data = self.valid_data
        invalid_data['first_name'] = ''

        response = self.client.post(
            reverse('user_create'),
            invalid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(User.objects.all())

    def test_do_not_create_user_without_last_name(self) -> None:
        invalid_data = self.valid_data
        invalid_data['last_name'] = ''

        response = self.client.post(
            reverse('user_create'),
            invalid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(User.objects.all())


class UserUpdateViewTest(TestCase):
    """"Test case for UserUpdateView"""

    fixtures = ['users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(User.objects.get(pk=1))
        self.valid_data = {
            'username': 'user_10',
            'first_name': 'First_name_user_10',
            'last_name': 'Last_name_user_10',
            'password1': 'password_10',
            'password2': 'password_10',
        }

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/users/1/update/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('user_update', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('user_update', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/user_create.html')

    def test_update_user_with_valid_data(self) -> None:
        response = self.client.post(
            reverse('user_update', args=[1]),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('users_list'))

        user = User.objects.get(pk=1)
        self.assertEqual(user.username, self.valid_data['username'])
        self.assertEqual(user.first_name, self.valid_data['first_name'])
        self.assertEqual(user.last_name, self.valid_data['last_name'])

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('User successfully updated'))
        self.assertEqual(message.tags, 'success')

    def test_do_not_update_user_without_username(self) -> None:
        user_before = User.objects.get(pk=1)
        invalid_data = self.valid_data
        invalid_data['username'] = ''

        response = self.client.post(
            reverse('user_update', args=[1]),
            invalid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        user_after = User.objects.get(pk=1)
        self.assertEqual(user_before, user_after)

    def test_do_not_update_user_without_first_name(self) -> None:
        user_before = User.objects.get(pk=1)
        invalid_data = self.valid_data
        invalid_data['first_name'] = ''

        response = self.client.post(
            reverse('user_update', args=[1]),
            invalid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        user_after = User.objects.get(pk=1)
        self.assertEqual(user_before, user_after)

    def test_do_not_update_user_without_last_name(self) -> None:
        user_before = User.objects.get(pk=1)
        invalid_data = self.valid_data
        invalid_data['last_name'] = ''

        response = self.client.post(
            reverse('user_update', args=[1]),
            invalid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        user_after = User.objects.get(pk=1)
        self.assertEqual(user_before, user_after)

    def test_do_not_update_another_user(self):
        user_before = User.objects.get(pk=2)

        response = self.client.post(
            reverse('user_update', args=[2]),
            self.valid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        user_after = User.objects.get(pk=2)
        self.assertEqual(user_before, user_after)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message,
            _('You do not have permission to change another user')
        )
        self.assertEqual(message.tags, 'error')

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()

        get_response = self.client.get(
            reverse('user_update', args=[1]),
            follow=True
        )
        self.assertRedirects(get_response, reverse('login'))

        message = list(get_response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')

        post_response = self.client.post(
            reverse('user_update', args=[1]),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(post_response, reverse('login'))

        message = list(post_response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')


class UserDeleteViewTest(TestCase):
    """"Test case for UserDeleteView"""

    fixtures = ['users.json', 'tasks.json', 'statuses.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(User.objects.get(pk=3))

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/users/3/delete/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('user_delete', args=[3]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('user_delete', args=[3]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/user_delete.html')

    def test_delete_user(self) -> None:
        length_of_user_list_before = len(User.objects.all())

        response = self.client.post(
            reverse('user_delete', args=[3]),
            follow=True
        )
        self.assertRedirects(response, reverse('users_list'))

        length_of_user_list_after = len(User.objects.all())
        self.assertTrue(
            length_of_user_list_after == length_of_user_list_before - 1
        )
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=3)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('User successfully deleted'))
        self.assertEqual(message.tags, 'success')

    def test_do_not_delete_another_user(self) -> None:
        user_before = User.objects.get(pk=2)

        response = self.client.post(
            reverse('user_delete', args=[2]),
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('users_list'))

        user_after = User.objects.get(pk=2)
        self.assertEqual(user_before, user_after)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message,
            _("Can't delete user because it's in use")
        )
        self.assertEqual(message.tags, 'error')

    def test_do_not_delete_user_linked_to_task(self) -> None:
        self.client.force_login(User.objects.get(pk=1))
        user_before = User.objects.get(pk=1)

        response = self.client.post(
            reverse('user_delete', args=[1]),
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('users_list'))

        user_after = User.objects.get(pk=1)
        self.assertEqual(user_before, user_after)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message,
            _("Can't delete user because it's in use")
        )
        self.assertEqual(message.tags, 'error')

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()

        get_response = self.client.get(
            reverse('user_delete', args=[1]),
            follow=True
        )
        self.assertRedirects(get_response, reverse('login'))

        message = list(get_response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')

        post_response = self.client.post(
            reverse('user_delete', args=[1]),
            follow=True
        )
        self.assertRedirects(post_response, reverse('login'))

        message = list(post_response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')
