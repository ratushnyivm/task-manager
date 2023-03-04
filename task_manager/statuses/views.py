from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from .models import Status

MSG_NO_PERMISSION = _('You are not authorized! Please sign in.')


class StatusesListView(LoginRequiredMixin, generic.ListView):

    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'

    def handle_no_permission(self):
        messages.warning(self.request, MSG_NO_PERMISSION)
        return redirect('login')


class StatusCreateView(LoginRequiredMixin,
                       SuccessMessageMixin,
                       generic.CreateView):

    model = Status
    fields = ['name']
    template_name = 'statuses/status_create.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('The status successfully created')
    extra_context = {
        'header': _('Create status'),
        'button': _('Create')
    }

    def handle_no_permission(self):
        messages.warning(self.request, MSG_NO_PERMISSION)
        return redirect('login')


class StatusUpdateView(LoginRequiredMixin,
                       SuccessMessageMixin,
                       generic.UpdateView):

    model = Status
    fields = ['name']
    template_name = 'statuses/status_create.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('The status successfully updated')
    extra_context = {
        'header': _('Update status'),
        'button': _('Change')
    }

    def handle_no_permission(self):
        messages.warning(self.request, MSG_NO_PERMISSION)
        return redirect('login')


class StatusDeleteView(LoginRequiredMixin,
                       SuccessMessageMixin,
                       generic.DeleteView):

    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('The status successfully deleted')

    def handle_no_permission(self):
        messages.warning(self.request, MSG_NO_PERMISSION)
        return redirect('login')
