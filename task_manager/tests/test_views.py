from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.test.utils import ignore_warnings
from django.urls import reverse
from django.utils.translation import gettext as _

User = get_user_model()

ignore_warnings(message="No directory at", module="whitenoise.base").enable()


class HomePageViewTest(TestCase):
    """Test case for the HomePageView."""

    def setUp(self) -> None:
        self.client = Client()

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'index.html')


class UserLoginViewTest(TestCase):
    """Test case for the UserLoginView."""

    fixtures = ['users.json']

    def setUp(self) -> None:
        self.client = Client()

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'login.html')

    def test_user_login(self):
        response = self.client.post(
            reverse('login'),
            {
                'username': 'user_1',
                'password': '123456789user_1',
            },
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.context['user'].is_authenticated)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('You are logged in'))
        self.assertEqual(message.tags, 'success')


class UserLogoutViewTest(TestCase):
    """Test case for the UserLogoutView."""

    fixtures = ['users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(User.objects.get(pk=1))

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/logout/', follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_user_logout(self):
        response = self.client.post(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('home'))

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('You are logged out'))
        self.assertEqual(message.tags, 'info')
