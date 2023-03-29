from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic
from task_manager.mixins import (
    CustomLoginRequiredMixin,
    DeletionProtectionMixin,
)

from .models import Status


class StatusListView(CustomLoginRequiredMixin, generic.ListView):
    """Generic class-based view for a list of statuses."""

    model = Status
    template_name = 'statuses/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       generic.CreateView):
    """Generic class-based view for creating statuses."""

    model = Status
    fields = ('name',)
    template_name = 'statuses/status_create.html'
    success_url = reverse_lazy('status_list')
    success_message = _('The status successfully created')
    extra_context = {
        'header': _('Create status'),
        'button': _('Create')
    }


class StatusUpdateView(CustomLoginRequiredMixin,
                       SuccessMessageMixin,
                       generic.UpdateView):
    """Generic class-based view for updating statuses."""

    model = Status
    fields = ('name',)
    template_name = 'statuses/status_create.html'
    success_url = reverse_lazy('status_list')
    success_message = _('The status successfully updated')
    extra_context = {
        'header': _('Update status'),
        'button': _('Update')
    }


class StatusDeleteView(CustomLoginRequiredMixin,
                       DeletionProtectionMixin,
                       SuccessMessageMixin,
                       generic.DeleteView):
    """Generic class-based view for deleting statuses."""

    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('status_list')
    success_message = _('The status successfully deleted')
    error_message = _("Can't delete status because it's in use")
