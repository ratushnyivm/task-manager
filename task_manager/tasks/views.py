from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views import generic
from django_filters.views import FilterView
from task_manager.mixins import CustomLoginRequiredMixin

from .filters import TaskFilter
from .models import Task

User = get_user_model()


class TaskListView(CustomLoginRequiredMixin, FilterView):
    """Generic class-based view for a list of tasks."""

    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    filterset_class = TaskFilter


class TaskCreateView(CustomLoginRequiredMixin,
                     SuccessMessageMixin,
                     generic.CreateView):
    """Generic class-based view for creating tasks."""

    model = Task
    fields = ('name', 'description', 'status', 'executor', 'labels')
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('task_list')
    success_message = _('The task successfully created')
    extra_context = {
        'header': _('Create task'),
        'button': _('Create')
    }

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskDetailView(CustomLoginRequiredMixin,
                     SuccessMessageMixin,
                     generic.DetailView):
    """Generic class-based view for detail displaying a task."""

    model = Task
    template_name = 'tasks/task_detail.html'
    extra_context = {
        'header': _('Task view'),
    }


class TaskUpdateView(CustomLoginRequiredMixin,
                     SuccessMessageMixin,
                     generic.UpdateView):
    """Generic class-based view for updating tasks."""

    model = Task
    fields = ('name', 'description', 'status', 'executor', 'labels')
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('task_list')
    success_message = _('The task successfully updated')
    extra_context = {
        'header': _('Update task'),
        'button': _('Update')
    }


class TaskDeleteView(CustomLoginRequiredMixin,
                     SuccessMessageMixin,
                     generic.DeleteView):
    """Generic class-based view for deleting tasks."""

    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('task_list')
    success_message = _('The task successfully deleted')
    error_message = _("The task can only be deleted by its author")

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.get_object().author.id and \
                request.user.is_authenticated:
            messages.error(self.request, self.error_message)
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
