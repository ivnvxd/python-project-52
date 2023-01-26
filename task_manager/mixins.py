from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.db.models import ProtectedError
from django.utils.translation import gettext as _


class AuthRequiredMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                request,
                _('You are not logged in! Please log in.')
            )
            return redirect(reverse_lazy('login'))

        return super().dispatch(request, *args, **kwargs)


class DeleteProtectionMixin:
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                request,
                _('It is not possible to delete a status because it is in use')
            )
            return redirect(reverse_lazy('login'))
