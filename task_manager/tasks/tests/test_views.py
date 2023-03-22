from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from django.urls import reverse
from django.utils.translation import gettext as _
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task
from task_manager.tasks.views import MSG_NO_PERMISSION

User = get_user_model()


class TaskListViewTest(TestCase):
    """Test case for the TaskListView."""

    fixtures = ['labels.json', 'statuses.json', 'tasks.json', 'users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(User.objects.get(pk=1))

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/tasks/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/tasks_list.html')

    def test_list_all_tasks(self) -> None:
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(len(response.context['tasks']), 3)

    def test_view_has_links_to_detail_and_update_and_delete(self) -> None:
        response = self.client.get(reverse('tasks_list'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        for task_id in range(1, len(response.context['tasks']) + 1):
            self.assertContains(response, f'/tasks/{task_id}/')
            self.assertContains(response, f'/tasks/{task_id}/update/')
            self.assertContains(response, f'/tasks/{task_id}/delete/')

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()
        response = self.client.get(reverse('tasks_list'), follow=True)
        self.assertRedirects(response, reverse('login'))

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')


class TaskCreateViewTest(TestCase):
    """"Test case for TaskCreateView."""

    fixtures = ['statuses.json', 'users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.author = User.objects.get(pk=1)
        self.client.force_login(self.author)
        self.valid_data = {
            'name': 'task_10',
            'description': 'description_10',
            'executor': 2,
            'status': 1,
        }

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/tasks/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('task_create'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/task_create.html')

    def test_create_task_with_valid_data(self) -> None:
        response = self.client.post(
            reverse('task_create'),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('tasks_list'))

        task = Task.objects.get(pk=1)
        self.assertEqual(task.name, self.valid_data['name'])
        self.assertEqual(task.description, self.valid_data['description'])
        self.assertEqual(task.author, self.author)
        self.assertEqual(
            task.executor,
            User.objects.get(pk=self.valid_data['executor'])
        )
        self.assertEqual(
            task.status,
            Status.objects.get(pk=self.valid_data['status'])
        )

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('The task successfully created'))
        self.assertEqual(message.tags, 'success')

    def test_create_task_without_description(self) -> None:
        valid_data = self.valid_data
        del valid_data['description']

        response = self.client.post(
            reverse('task_create'),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('tasks_list'))

        task = Task.objects.get(pk=1)
        self.assertEqual(task.name, self.valid_data['name'])
        self.assertEqual(task.description, '')
        self.assertEqual(task.author, self.author)
        self.assertEqual(
            task.executor,
            User.objects.get(pk=self.valid_data['executor'])
        )
        self.assertEqual(
            task.status,
            Status.objects.get(pk=self.valid_data['status'])
        )

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('The task successfully created'))
        self.assertEqual(message.tags, 'success')

    def test_create_task_without_executor(self) -> None:
        valid_data = self.valid_data
        del valid_data['executor']

        response = self.client.post(
            reverse('task_create'),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('tasks_list'))

        task = Task.objects.get(pk=1)
        self.assertEqual(task.name, self.valid_data['name'])
        self.assertEqual(task.description, self.valid_data['description'])
        self.assertEqual(task.author, self.author)
        self.assertIsNone(task.executor)
        self.assertEqual(
            task.status,
            Status.objects.get(pk=self.valid_data['status'])
        )

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('The task successfully created'))
        self.assertEqual(message.tags, 'success')

    def test_do_not_create_task_without_name(self) -> None:
        invalid_data = self.valid_data
        invalid_data['name'] = ''

        response = self.client.post(
            reverse('task_create'),
            invalid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(Task.objects.all())

    def test_do_not_create_task_without_status(self) -> None:
        invalid_data = self.valid_data
        del invalid_data['status']

        response = self.client.post(
            reverse('task_create'),
            invalid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(Task.objects.all())

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()
        response = self.client.get(reverse('task_create'), follow=True)
        self.assertRedirects(response, reverse('login'))

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')


class TaskDetailViewTest(TestCase):
    """"Test case for TaskDetailView."""

    fixtures = ['labels.json', 'statuses.json', 'tasks.json', 'users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(User.objects.get(pk=1))

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/tasks/1/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('task_detail', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('task_detail', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/task_detail.html')

    def test_view_has_all_data(self) -> None:
        task = Task.objects.get(pk=1)

        response = self.client.get(reverse('task_detail', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, task.name)
        self.assertContains(response, task.description)
        self.assertContains(response, task.author)
        self.assertContains(response, task.executor)
        self.assertContains(response, task.status)
        self.assertContains(
            response,
            task.created_at.strftime("%d.%m.%Y %H:%M")
        )

    def test_view_has_links_to_update_and_delete(self) -> None:
        response = self.client.get(reverse('task_detail', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, f'/tasks/{1}/update/')
        self.assertContains(response, f'/tasks/{1}/delete/')

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()

        response = self.client.get(
            reverse('task_detail', args=[1]),
            follow=True
        )
        self.assertRedirects(response, reverse('login'))

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')


class TaskUpdateViewTest(TestCase):
    """"Test case for TaskUpdateView."""

    fixtures = ['labels.json', 'statuses.json', 'tasks.json', 'users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.author = User.objects.get(pk=1)
        self.client.force_login(self.author)
        self.valid_data = {
            'name': 'task_10',
            'description': 'description_10',
            'executor': 2,
            'status': 1,
        }

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/tasks/1/update/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('task_update', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('task_update', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/task_create.html')

    def test_update_task_with_valid_data(self) -> None:
        response = self.client.post(
            reverse('task_update', args=[1]),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('tasks_list'))

        task = Task.objects.get(pk=1)
        self.assertEqual(task.name, self.valid_data['name'])
        self.assertEqual(task.description, self.valid_data['description'])
        self.assertEqual(task.author, self.author)
        self.assertEqual(
            task.executor,
            User.objects.get(pk=self.valid_data['executor'])
        )
        self.assertEqual(
            task.status,
            Status.objects.get(pk=self.valid_data['status'])
        )

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('The task successfully updated'))
        self.assertEqual(message.tags, 'success')

    def test_update_task_without_description(self) -> None:
        valid_data = self.valid_data
        del valid_data['description']

        response = self.client.post(
            reverse('task_update', args=[1]),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('tasks_list'))

        task = Task.objects.get(pk=1)
        self.assertEqual(task.name, self.valid_data['name'])
        self.assertEqual(task.description, '')
        self.assertEqual(task.author, self.author)
        self.assertEqual(
            task.executor,
            User.objects.get(pk=self.valid_data['executor'])
        )
        self.assertEqual(
            task.status,
            Status.objects.get(pk=self.valid_data['status'])
        )

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('The task successfully updated'))
        self.assertEqual(message.tags, 'success')

    def test_update_task_without_executor(self) -> None:
        valid_data = self.valid_data
        del valid_data['executor']

        response = self.client.post(
            reverse('task_update', args=[1]),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(response, reverse('tasks_list'))

        task = Task.objects.get(pk=1)
        self.assertEqual(task.name, self.valid_data['name'])
        self.assertEqual(task.description, self.valid_data['description'])
        self.assertEqual(task.author, self.author)
        self.assertIsNone(task.executor)
        self.assertEqual(
            task.status,
            Status.objects.get(pk=self.valid_data['status'])
        )

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('The task successfully updated'))
        self.assertEqual(message.tags, 'success')

    def test_do_not_update_task_without_name(self) -> None:
        task_before = Task.objects.get(pk=1)
        invalid_data = self.valid_data
        invalid_data['name'] = ''

        response = self.client.post(
            reverse('task_update', args=[1]),
            invalid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        task_after = Task.objects.get(pk=1)
        self.assertEqual(task_before, task_after)

    def test_do_not_create_task_without_status(self) -> None:
        task_before = Task.objects.get(pk=1)
        invalid_data = self.valid_data
        del invalid_data['status']

        response = self.client.post(
            reverse('task_update', args=[1]),
            invalid_data,
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

        task_after = Task.objects.get(pk=1)
        self.assertEqual(task_before, task_after)

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()

        get_response = self.client.get(
            reverse('task_update', args=[1]),
            follow=True
        )
        self.assertRedirects(get_response, reverse('login'))

        message = list(get_response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')

        post_response = self.client.post(
            reverse('task_update', args=[1]),
            self.valid_data,
            follow=True
        )
        self.assertRedirects(post_response, reverse('login'))

        message = list(post_response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')


class TaskDeleteViewTest(TestCase):
    """"Test case for TaskDeleteView."""

    fixtures = ['labels.json', 'statuses.json', 'tasks.json', 'users.json']

    def setUp(self) -> None:
        self.client = Client()
        self.client.force_login(User.objects.get(pk=1))

    def test_view_url_exists_at_desired_location(self) -> None:
        response = self.client.get('/tasks/1/delete/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_url_accessible_by_name(self) -> None:
        response = self.client.get(reverse('task_delete', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_view_uses_correct_template(self) -> None:
        response = self.client.get(reverse('task_delete', args=[1]))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'tasks/task_delete.html')

    def test_delete_task(self) -> None:
        length_of_task_list_before = len(Task.objects.all())

        response = self.client.post(
            reverse('task_delete', args=[1]),
            follow=True
        )
        self.assertRedirects(response, reverse('tasks_list'))

        length_of_task_list_after = len(Task.objects.all())
        self.assertTrue(
            length_of_task_list_after == length_of_task_list_before - 1
        )
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=1)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(message.message, _('The task successfully deleted'))
        self.assertEqual(message.tags, 'success')

    def test_do_not_delete_task_of_other_authors(self):
        task_before = Task.objects.get(pk=2)

        response = self.client.post(
            reverse('task_delete', args=[2]),
            follow=True
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertRedirects(response, reverse('tasks_list'))

        task_after = Task.objects.get(pk=2)
        self.assertEqual(task_before, task_after)

        message = list(response.context.get('messages'))[0]
        self.assertEqual(
            message.message,
            _("The task can only be deleted by its author")
        )
        self.assertEqual(message.tags, 'error')

    def test_redirect_if_not_logged_in(self) -> None:
        self.client.logout()

        get_response = self.client.get(
            reverse('task_delete', args=[1]),
            follow=True
        )
        self.assertRedirects(get_response, reverse('login'))

        message = list(get_response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')

        post_response = self.client.post(
            reverse('task_delete', args=[1]),
            follow=True
        )
        self.assertRedirects(post_response, reverse('login'))

        message = list(post_response.context.get('messages'))[0]
        self.assertEqual(message.message, MSG_NO_PERMISSION)
        self.assertEqual(message.tags, 'error')
