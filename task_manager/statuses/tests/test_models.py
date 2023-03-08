from django.test import TestCase
from django.utils.translation import gettext as _
from task_manager.statuses.models import Status


class StatusesModelTest(TestCase):

    def setUp(self) -> None:
        Status.objects.create(name='status')
        self.status = Status.objects.get(pk=1)

    def test_name_label(self) -> None:
        field_label = self.status._meta.get_field('name').verbose_name
        self.assertEqual(field_label, _('name'))

    def test_name_max_length(self) -> None:
        max_length = self.status._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)

    def test_name_unique(self) -> None:
        unique = self.status._meta.get_field('name').unique
        self.assertEqual(unique, True)

    def test_name_blank(self) -> None:
        blank = self.status._meta.get_field('name').blank
        self.assertEqual(blank, False)

    def test_created_at_label(self) -> None:
        field_label = self.status._meta.get_field('created_at').verbose_name
        self.assertEqual(field_label, _('created at'))

    def test_created_at_auto_now_add(self) -> None:
        auto_now_add = self.status._meta.get_field('created_at').auto_now_add
        self.assertEqual(auto_now_add, True)

    def test_representation(self) -> None:
        self.assertEqual(self.status.__str__(), 'status')
