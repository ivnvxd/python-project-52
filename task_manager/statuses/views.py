from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin
from .models import Status
from .forms import StatusForm


class StatusesListView(AuthRequiredMixin, ListView):
    """
    Show all statuses.

    Authorization required.
    """
    template_name = 'statuses/statuses.html'
    model = Status
    context_object_name = 'statuses'
    extra_context = {
        'title': _('Statuses')
    }


class StatusCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    """
    Create new status.

    Authorisation required.
    """
    template_name = 'form.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully created')
    extra_context = {
        'title': _('Create status'),
        'button_text': _('Create'),
    }


class StatusUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    """
    Edit existing status.

    Authorisation required.
    """
    template_name = 'form.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully changed')
    extra_context = {
        'title': _('Change status'),
        'button_text': _('Change'),
    }


class StatusDeleteView(AuthRequiredMixin, DeleteProtectionMixin,
                       SuccessMessageMixin, DeleteView):
    """
    Delete existing status.

    Authorization required.
    If the status is associated with at least one task it cannot be deleted.
    """
    template_name = 'statuses/delete.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted')
    protected_message = _('It is not possible to delete a status '
                          'because it is in use')
    protected_url = reverse_lazy('statuses')
    extra_context = {
        'title': _('Delete status'),
        'button_text': _('Yes, delete'),
    }
