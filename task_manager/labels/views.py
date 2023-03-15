from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic

from .models import Label

MSG_NO_PERMISSION = _('You are not authorized! Please sign in.')


class LabelListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view for a list of labels."""

    model = Label
    template_name = 'labels/label_list.html'
    context_object_name = 'labels'

    def handle_no_permission(self):
        messages.error(self.request, MSG_NO_PERMISSION)
        return redirect('login')


class LabelCreateView(LoginRequiredMixin,
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

    def handle_no_permission(self):
        messages.error(self.request, MSG_NO_PERMISSION)
        return redirect('login')


class LabelUpdateView(LoginRequiredMixin,
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

    def handle_no_permission(self):
        messages.error(self.request, MSG_NO_PERMISSION)
        return redirect('login')


class LabelDeleteView(LoginRequiredMixin,
                      SuccessMessageMixin,
                      generic.DeleteView):
    """Generic class-based view for deleting label."""

    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('label_list')
    success_message = _('The label successfully deleted')
    unsuccess_message = _("Can't delete label because it's in use")

    def handle_no_permission(self):
        messages.error(self.request, MSG_NO_PERMISSION)
        return redirect('login')

    def form_valid(self, form):
        try:
            self.object.delete()
            messages.success(self.request, self.success_message)
            return redirect(self.success_url)
        except ProtectedError:
            messages.error(self.request, self.unsuccess_message)
            return redirect(self.success_url)
