from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

MAX_LENGTH = 150


class CustomUser(AbstractUser):
    """Model representing a user."""

    first_name = models.CharField(
        max_length=MAX_LENGTH,
        blank=False,
        verbose_name=_('first name')
    )
    last_name = models.CharField(
        max_length=MAX_LENGTH,
        blank=False,
        verbose_name=_('last name')
    )

    def __str__(self):
        return self.get_full_name()
