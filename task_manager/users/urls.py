from django.urls import path

from .views import UsersListView, UserCreateView, UserUpdateView, UserDeleteView


urlpatterns = [
    path('', UsersListView.as_view(), name='users'),
    path('create/', UserCreateView.as_view(), name='sign_up'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]
