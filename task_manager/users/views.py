from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from .forms import UserCreationAndChangeForm

User = get_user_model()


class UserListView(generic.ListView):

    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, generic.CreateView):

    model = User
    form_class = UserCreationAndChangeForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('login')
    success_message = _('User successfully registered')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Register')
        return context


class UserUpdateView(SuccessMessageMixin, generic.UpdateView):

    model = User
    form_class = UserCreationAndChangeForm
    template_name = 'users/form.html'
    success_url = reverse_lazy('users_index')
    success_message = _('User successfully changed')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = _('Change')
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().id:
            messages.error(
                self.request,
                _('You do not have permission to change another user')
            )
            return redirect('users_index')
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(generic.DeleteView):

    model = User
    template_name = 'users/user_delete.html'
    context_object_name = 'user'
    success_url = reverse_lazy('users_index')

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().id:
            messages.error(
                self.request,
                _("Can't delete user because it's in use")
            )
            return redirect('users_index')
        return super().dispatch(request, *args, **kwargs)
