from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class UserPermissionMixin(UserPassesTestMixin):
    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(
            self.request,
            _("You have no rights to change another user.")
        )
        return redirect(reverse_lazy('users'))
