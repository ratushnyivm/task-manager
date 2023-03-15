from django.db import models
from django.utils.translation import gettext as _

MAX_LENGTH = 50


class Label(models.Model):
    """Model representing a label."""

    name = models.CharField(
        verbose_name=_('name'),
        max_length=MAX_LENGTH,
        unique=True,
        blank=False,
    )
    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _('label')
        verbose_name_plural = _('labels')

    def __str__(self):
        return self.name
