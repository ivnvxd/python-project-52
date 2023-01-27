from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.utils.translation import gettext as _


class AuthRequiredMixin(LoginRequiredMixin):
    """
    Authentication check.
    Restricts access without authentication.
    """
    auth_message = _('You are not logged in! Please log in.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.auth_message)
            return redirect(reverse_lazy('login'))

        return super().dispatch(request, *args, **kwargs)


class UserPermissionMixin(UserPassesTestMixin):
    """
    Authorisation check.
    Prohibits changing an item created by another user.
    """
    permission_message = None
    permission_url = None

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class DeleteProtectionMixin:
    """
    Association check.
    Prohibits deleting an object if it is used by other objects.
    """
    protected_message = None
    protected_url = None

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)


class AuthorDeletionMixin(UserPassesTestMixin):
    """
    Authorisation check.
    Prohibits deleting an item not by its author.
    """
    author_message = None
    author_url = None

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.author_message)
        return redirect(self.author_url)

    # Another way using dispatch function without UserPassesTestMixin:

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.id != self.get_object().author.id:
    #         messages.error(self.request, self.author_message)
    #         return redirect(self.author_url)
    #     return super().dispatch(request, *args, **kwargs)
