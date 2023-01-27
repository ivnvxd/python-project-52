from django import forms
from django.utils.translation import gettext as _

from .models import Label


class LabelForm(forms.ModelForm):

    name = forms.CharField(
        max_length=150, required=True, label=_("Name")
    )

    class Meta:
        model = Label
        fields = ('name',)
