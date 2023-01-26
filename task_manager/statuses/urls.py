from django.urls import path

from .views import StatusesListView, StatusCreateView,\
    StatusUpdateView, StatusDeleteView


urlpatterns = [
    path('', StatusesListView.as_view(), name='statuses'),
    path('create/', StatusCreateView.as_view(), name='status_create'),
    path('<int:pk>/update/', StatusUpdateView.as_view(), name='status_update'),
    path('<int:pk>/delete/', StatusDeleteView.as_view(), name='status_delete'),
]
