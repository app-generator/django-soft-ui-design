from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.home.models import Worker, Task, TaskType, Position


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("position", "profile_image")
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position", "profile_image")}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            (
                "Additional info",
                {"fields": ("first_name", "last_name", "position", "profile_image")},
            ),
        )
    )


admin.site.register(Task)
admin.site.register(TaskType)
admin.site.register(Position)
