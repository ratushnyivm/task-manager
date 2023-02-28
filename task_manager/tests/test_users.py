from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.test.utils import ignore_warnings
from django.urls import reverse

User = get_user_model()

ignore_warnings(message="No directory at", module="whitenoise.base").enable()


class CustomUserTestCase(TestCase):

    fixtures = ['users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.user1 = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)
        self.user3 = User.objects.get(pk=3)
        self.valid_form_data = {
            'username': 'user_10',
            'first_name': 'First_name_user_10',
            'last_name': 'Last_name_user_10',
            'password1': 'password_10',
            'password2': 'password_10',
        }

    def test_users_model(self) -> None:
        response = self.client.get(reverse('users_index'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

        users_list = list(response.context['users'])
        self.assertTrue(len(users_list) == 3)

        user1, user2, user3 = users_list
        self.assertEqual(user1.username, 'user_1')
        self.assertEqual(user2.first_name, 'First_name_user_2')
        self.assertEqual(user3.last_name, 'Last_name_user_3')
        self.assertEqual(user1.__str__(), 'First_name_user_1 Last_name_user_1')

    def test_users_create_view(self):
        get_response = self.client.get(reverse('user_create'))
        self.assertEqual(get_response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(get_response, 'users/form.html')

        post_response = self.client.post(
            path=reverse('user_create'),
            data=self.valid_form_data,
            follow=True,
        )

        self.assertEqual(post_response.status_code, HTTPStatus.OK)
        self.assertRedirects(post_response, reverse('login'))
        self.assertTrue(User.objects.get(pk=4))

    def test_user_update_view(self):
        self.client.force_login(self.user1)
        update_user_path = reverse('user_update', args=[1])

        get_response = self.client.get(update_user_path)
        self.assertEqual(get_response.status_code, HTTPStatus.OK)

        post_response = self.client.post(
            path=update_user_path,
            data=self.valid_form_data,
            follow=True,
        )
        self.assertEqual(post_response.status_code, HTTPStatus.OK)
        self.assertRedirects(post_response, reverse('users_index'))

        user1_update = User.objects.get(pk=1)
        self.assertEqual(
            user1_update.username, self.valid_form_data['username']
        )
        self.assertEqual(
            user1_update.first_name, self.valid_form_data['first_name']
        )
        self.assertEqual(
            user1_update.last_name, self.valid_form_data['last_name']
        )

    def test_user_delete_view(self):
        self.client.force_login(self.user3)
        delete_user_path = reverse('user_delete', args=[3])
        users_count_before_delete = User.objects.count()

        get_response = self.client.get(delete_user_path)
        self.assertEqual(get_response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(get_response, 'users/user_delete.html')
        users_count_after_delete = User.objects.count()
        self.assertTrue(users_count_before_delete == users_count_after_delete)

        post_response = self.client.post(delete_user_path)
        self.assertEqual(post_response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(post_response, reverse('users_index'))
        users_count_after_delete = User.objects.count()
        self.assertTrue(
            users_count_after_delete == users_count_before_delete - 1
        )
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(pk=3)
