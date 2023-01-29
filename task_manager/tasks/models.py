from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.labels.models import Label


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
        verbose_name=_('Name')
    )
    description = models.TextField(
        max_length=10000,
        blank=True,
        verbose_name=_('Description')
    )
    date_created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Creation date')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author',
        verbose_name=_('Author')
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
        related_name='statuses',
        verbose_name=_('Status')
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor',
        verbose_name=_('Executor')
    )
    labels = models.ManyToManyField(
        Label,
        through='TaskLabelRelation',
        through_fields=('task', 'label'),
        blank=True,
        related_name='labels',
        verbose_name=_('Labels')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class TaskLabelRelation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
