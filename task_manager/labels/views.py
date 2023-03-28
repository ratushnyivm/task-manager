from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic
from task_manager.mixins import (
    CustomLoginRequiredMixin,
    DeletionProtectionMixin,
)

from .models import Label


class LabelListView(CustomLoginRequiredMixin, generic.ListView):
    """Generic class-based view for a list of labels."""

    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'


class LabelCreateView(CustomLoginRequiredMixin,
                      SuccessMessageMixin,
                      generic.CreateView):
    """Generic class-based view for creating label."""

    model = Label
    fields = ('name',)
    template_name = 'labels/label_create.html'
    success_url = reverse_lazy('label_list')
    success_message = _('The label successfully created')
    extra_context = {
        'header': _('Create label'),
        'button': _('Create')
    }


class LabelUpdateView(CustomLoginRequiredMixin,
                      SuccessMessageMixin,
                      generic.UpdateView):
    """Generic class-based view for updating label."""

    model = Label
    fields = ('name',)
    template_name = 'labels/label_create.html'
    success_url = reverse_lazy('label_list')
    success_message = _('The label successfully updated')
    extra_context = {
        'header': _('Update label'),
        'button': _('Update')
    }


class LabelDeleteView(CustomLoginRequiredMixin,
                      DeletionProtectionMixin,
                      SuccessMessageMixin,
                      generic.DeleteView):
    """Generic class-based view for deleting label."""

    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('label_list')
    success_message = _('The label successfully deleted')
    error_message = _("Can't delete label because it's in use")
