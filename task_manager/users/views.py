from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic
from task_manager.mixins import (
    CustomLoginRequiredMixin,
    DeletionProtectionMixin,
)

from .forms import UserCreationAndChangeForm

User = get_user_model()


class UsersListView(generic.ListView):
    """Generic class-based view for a list of users."""

    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, generic.CreateView):
    """Generic class-based view for creating users."""

    model = User
    form_class = UserCreationAndChangeForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')
    extra_context = {
        'header': _('Sign up'),
        'button': _('Register')
    }


class UserUpdateView(CustomLoginRequiredMixin,
                     SuccessMessageMixin,
                     generic.UpdateView):
    """Generic class-based view for updating users."""

    model = User
    form_class = UserCreationAndChangeForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('user_list')
    success_message = _('User successfully updated')
    extra_context = {
        'header': _('Update user'),
        'button': _('Update')
    }

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().id and \
                request.user.is_authenticated:
            messages.error(
                self.request,
                _('You do not have permission to change another user')
            )
            return redirect('user_list')
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(CustomLoginRequiredMixin,
                     DeletionProtectionMixin,
                     SuccessMessageMixin,
                     generic.DeleteView):
    """Generic class-based view for deleting users."""

    model = User
    template_name = 'users/user_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('user_list')
    success_message = _('User successfully deleted')
    error_message = _("Can't delete user because it's in use")

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().id and \
                request.user.is_authenticated:
            messages.error(self.request, self.error_message)
            return redirect('user_list')
        return super().dispatch(request, *args, **kwargs)
