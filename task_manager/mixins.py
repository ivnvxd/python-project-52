from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
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