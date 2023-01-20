# from django.shortcuts import render
# from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from task_manager.users.models import Users


class UsersListView(ListView):
    template_name = 'users/users.html'
    model = Users

    # def get(self, request, *args, **kwargs):
    #     users = Users.objects.all()
    #     return render(request, 'users/users.html', context={
    #         'users': users,
    #     })


class UserCreateView(CreateView):
    pass


class UserUpdateView(UpdateView):
    pass


class UserDeleteView(DeleteView):
    pass
