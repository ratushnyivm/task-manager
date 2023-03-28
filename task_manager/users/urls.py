from django.urls import path

from .views import (
    UserCreateView,
    UserDeleteView,
    UsersListView,
    UserUpdateView,
)

urlpatterns = [
    path('', UsersListView.as_view(), name='user_list'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/update/', UserUpdateView.as_view(), name='user_update'),
    path('<int:pk>/delete/', UserDeleteView.as_view(), name='user_delete'),
]
