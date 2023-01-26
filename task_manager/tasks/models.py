from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.users.models import User
from task_manager.statuses.models import Status


class Task(models.Model):
    name = models.CharField(
        max_length=150,
        blank=False,
        unique=True,
        verbose_name=_('Task name')
    )
    description = models.TextField(
        blank=True,
        verbose_name=_('Description')
    )
    created_date = models.DateTimeField(
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
        verbose_name=_('Status')
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor',
        verbose_name=_('Executor')
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')
