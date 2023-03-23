import django_filters
from django.forms import CheckboxInput
from django.utils.translation import gettext as _
from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class TaskFilter(django_filters.FilterSet):

    label = django_filters.ModelChoiceFilter(
        field_name="labels",
        label=_("Label"),
        queryset=Label.objects.all(),
    )
    self_tasks = django_filters.BooleanFilter(
        method="get_self_tasks",
        label=_("My tasks only"),
        widget=CheckboxInput,
    )

    def get_self_tasks(self, queryset, field_name, value):
        if value:
            return queryset.filter(author=self.request.user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor']
