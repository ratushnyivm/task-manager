from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext as _
from task_manager.labels.models import Label
from task_manager.statuses.models import Status

User = get_user_model()

MAX_LENGTH = 100


class Task(models.Model):
    """Model representing a task."""

    name = models.CharField(
        verbose_name=_('name'),
        max_length=MAX_LENGTH,
    )
    description = models.TextField(
        verbose_name=_('description'),
        blank=True,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('author'),
        related_name='author',
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        verbose_name=_('executor'),
        related_name='executor',
        blank=True,
        null=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        verbose_name=_('status'),
        related_name='status',
        null=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_('created at'),
        auto_now_add=True,
    )
    labels = models.ManyToManyField(
        Label,
        verbose_name=_('labels'),
        blank=True,
        through='TaskLabel',
        through_fields=('task', 'label'),
    )

    class Meta:
        verbose_name = _('task')
        verbose_name_plural = _('tasks')

    def __str__(self):
        return self.name


class TaskLabel(models.Model):
    """Model representing intermediary table linking tasks to labels."""

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
    )
    label = models.ForeignKey(
        Label,
        on_delete=models.PROTECT,
    )
