from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from .forms import UserCreationAndChangeForm

User = get_user_model()

MSG_NO_PERMISSION = _('You are not authorized! Please sign in.')


class UsersListView(generic.ListView):
    """Generic class-based view for a list of users."""

    model = User
    template_name = 'users/users_list.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, generic.CreateView):
    """Generic class-based view for creating users."""

    model = User
    form_class = UserCreationAndChangeForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')
    extra_context = {
        'header': _('Registration'),
        'button': _('Register')
    }


class UserUpdateView(LoginRequiredMixin,
                     SuccessMessageMixin,
                     generic.UpdateView):
    """Generic class-based view for updating users."""

    model = User
    form_class = UserCreationAndChangeForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('users_list')
    success_message = _('User successfully updated')
    extra_context = {
        'header': _('Update user'),
        'button': _('Update')
    }

    def handle_no_permission(self):
        messages.error(self.request, MSG_NO_PERMISSION)
        return redirect('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().id and \
              request.user.is_authenticated:
            messages.error(
                self.request,
                _('You do not have permission to change another user')
            )
            return redirect('users_list')
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin,
                     SuccessMessageMixin,
                     generic.DeleteView):
    """Generic class-based view for deleting users."""

    model = User
    template_name = 'users/user_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users_list')
    success_message = _('User successfully deleted')
    unsuccess_message = _("Can't delete user because it's in use")

    def handle_no_permission(self):
        messages.error(self.request, MSG_NO_PERMISSION)
        return redirect('login')

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().id and \
              request.user.is_authenticated:
            messages.error(self.request, self.unsuccess_message)
            return redirect('users_list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(self.request, self.unsuccess_message)
            return redirect(self.success_url)
