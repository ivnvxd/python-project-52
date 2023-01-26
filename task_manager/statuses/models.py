from django.db import models
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    name = models.CharField(
        verbose_name=_('name'),
        max_length=150,
        unique=True,
        blank=False
    )
    date_created = models.DateTimeField(
        verbose_name=_('Creation date'),
        auto_now_add=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Status')
        verbose_name_plural = _('Statuses')
