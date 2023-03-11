from django.test import TestCase
from django.utils.translation import gettext as _
from task_manager.users.models import CustomUser


class CustomUserModelTest(TestCase):
    """Test case for the CustomUser model."""

    def setUp(self) -> None:
        CustomUser.objects.create(
            username='user_10',
            first_name='First_name_user_10',
            last_name='Last_name_user_10',
            password='password_10',
        )
        self.user = CustomUser.objects.get(pk=1)

    def test_first_name_label(self) -> None:
        field_label = self.user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, _('first name'))

    def test_first_name_max_length(self) -> None:
        max_length = self.user._meta.get_field('first_name').max_length
        self.assertEqual(max_length, 150)

    def test_first_name_blank(self) -> None:
        blank = self.user._meta.get_field('first_name').blank
        self.assertEqual(blank, False)

    def test_last_name_label(self) -> None:
        field_label = self.user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, _('last name'))

    def test_last_name_max_length(self) -> None:
        max_length = self.user._meta.get_field('last_name').max_length
        self.assertEqual(max_length, 150)

    def test_last_name_blank(self) -> None:
        blank = self.user._meta.get_field('last_name').blank
        self.assertEqual(blank, False)

    def test_representation(self) -> None:
        self.assertEqual(
            self.user.__str__(),
            'First_name_user_10 Last_name_user_10'
        )
