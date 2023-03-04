from django.db import models
from django.utils.translation import gettext as _


class Status(models.Model):
    name = models.CharField(
        max_length=100,
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
