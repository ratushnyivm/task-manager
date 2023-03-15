from django.contrib import admin

from .models import Label


@admin.register(Label)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
