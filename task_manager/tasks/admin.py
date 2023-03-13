from django.contrib import admin

from .models import Task


@admin.register(Task)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'author', 'executor', 'created_at')
