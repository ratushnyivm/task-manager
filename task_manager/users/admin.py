from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UserCreationAndChangeForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationAndChangeForm
    form = UserCreationAndChangeForm
    model = CustomUser
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
