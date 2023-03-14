from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.translation import gettext as _
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task

User = get_user_model()


class TaskModelTest(TestCase):
    """Test case for the Task model."""

    def setUp(self) -> None:
        User.objects.create(
            username='user_10',
            first_name='First_name_user_10',
            last_name='Last_name_user_10',
            password='password_10',
        )
        self.author = User.objects.get(pk=1)

        User.objects.create(
            username='user_20',
            first_name='First_name_user_20',
            last_name='Last_name_user_20',
            password='password_20',
        )
        self.executor = User.objects.get(pk=2)

        Status.objects.create(name='status')
        self.status = Status.objects.get(pk=1)

        Task.objects.create(
            name='task_10',
            description='description_10',
            author=self.author,
            executor=self.executor,
            status=self.status
        )
        self.task = Task.objects.get(pk=1)

    def test_name_label(self) -> None:
        field_label = self.task._meta.get_field('name').verbose_name
        self.assertEqual(field_label, _('name'))

    def test_name_max_length(self) -> None:
        max_length = self.status._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_description_label(self) -> None:
        field_label = self.task._meta.get_field('description').verbose_name
        self.assertEqual(field_label, _('description'))

    def test_description_blank(self) -> None:
        blank = self.task._meta.get_field('description').blank
        self.assertEqual(blank, True)

    def test_author_label(self) -> None:
        field_label = self.task._meta.get_field('author').verbose_name
        self.assertEqual(field_label, _('author'))

    def test_author_model(self) -> None:
        model = self.task._meta.get_field('author').related_model
        self.assertEqual(model, User)

    def test_author_related_name(self) -> None:
        self.assertEqual(self.task.author, self.author)

    def test_executor_label(self) -> None:
        field_label = self.task._meta.get_field('executor').verbose_name
        self.assertEqual(field_label, _('executor'))

    def test_executor_model(self) -> None:
        model = self.task._meta.get_field('executor').related_model
        self.assertEqual(model, User)

    def test_executor_related_name(self) -> None:
        self.assertEqual(self.task.executor, self.executor)

    def test_executor_blank(self) -> None:
        blank = self.task._meta.get_field('executor').blank
        self.assertEqual(blank, True)

    def test_executor_null(self) -> None:
        blank = self.task._meta.get_field('executor').null
        self.assertEqual(blank, True)

    def test_status_label(self) -> None:
        field_label = self.task._meta.get_field('status').verbose_name
        self.assertEqual(field_label, _('status'))

    def test_status_model(self) -> None:
        model = self.task._meta.get_field('status').related_model
        self.assertEqual(model, Status)

    def test_status_related_name(self) -> None:
        self.assertEqual(self.task.status, self.status)

    def test_status_null(self) -> None:
        blank = self.task._meta.get_field('status').null
        self.assertEqual(blank, True)

    def test_created_at_label(self) -> None:
        field_label = self.task._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, _('created at'))

    def test_created_at_auto_now_add(self) -> None:
        auto_now_add = self.task._meta.get_field('created_at').auto_now_add
        self.assertEqual(auto_now_add, True)

    def test_representation(self) -> None:
        self.assertEqual(self.task.__str__(), 'task_10')
