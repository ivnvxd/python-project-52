from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin

from task_manager.mixins import AuthRequiredMixin
from .models import Status
from .forms import StatusForm


class StatusesListView(AuthRequiredMixin, ListView):
    template_name = 'statuses/statuses.html'
    model = Status
    context_object_name = 'statuses'
    extra_context = {
        'title': _('Statuses')
    }


class StatusCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
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
    login_url = reverse_lazy('login')
    template_name = 'form.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully changed')
    extra_context = {
        'title': _('Status change'),
        'button_text': _('Change'),
    }


class StatusDeleteView(AuthRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = 'statuses/delete.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted')
    extra_context = {
        'title': _('Delete status'),
        'button_text': _('Yes, delete'),
    }
