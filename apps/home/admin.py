# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.home.models import (
    Worker,
    Task,
    TaskType,
    Position
)


@admin.register(Worker)
class DriverAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position",)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (("Additional info", {"fields": ("first_name", "last_name", "position",)}),)
    )


admin.site.register(Task)
admin.site.register(TaskType)
admin.site.register(Position)
