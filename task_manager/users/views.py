from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy

from .models import User
from .forms import UserRegistrationForm


class UsersListView(ListView):
    template_name = 'users/users.html'
    model = User
    context_object_name = 'users'
    extra_context = {
        'title': _('Users')
    }


class UserCreateView(CreateView):
    template_name = 'users/create.html'
    model = User
    form_class = UserRegistrationForm
    success_url = reverse_lazy('home')
    success_message = _('User created successfully')
    extra_context = {
        'title': _('Create user'),
        'description': _('User registration'),
        'button_text': _('Register'),
    }


class UserUpdateView(UpdateView):
    pass


class UserDeleteView(DeleteView):
    pass
