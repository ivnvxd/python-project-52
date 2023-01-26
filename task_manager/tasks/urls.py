from django.urls import path

from .views import TasksListView, TaskCreateView,\
    TaskUpdateView, TaskDeleteView


urlpatterns = [
    path('', TasksListView.as_view(), name='tasks'),
    path('create/', TaskCreateView.as_view(), name='task_create'),
    path('<int:pk>/update/', TaskUpdateView.as_view(), name='task_update'),
    path('<int:pk>/delete/', TaskDeleteView.as_view(), name='task_delete'),
]
