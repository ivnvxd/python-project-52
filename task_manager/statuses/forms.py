from django import forms
from django.utils.translation import gettext as _

from .models import Status


class StatusForm(forms.ModelForm):

    name = forms.CharField(
        max_length=150, required=True, label=_("Name")
    )

    class Meta:
        model = Status
        fields = ('name',)
