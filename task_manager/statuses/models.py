from django.db import models
from django.utils.translation import gettext as _

MAX_LENGTH = 100


class Status(models.Model):
    """Model representing a status."""

    name = models.CharField(
        max_length=MAX_LENGTH,
        unique=True,
        blank=False,
        verbose_name=_('name')
    )
    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _('status')
        verbose_name_plural = _('statuses')

    def __str__(self):
        return self.name
