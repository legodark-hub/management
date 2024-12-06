from django.contrib import admin

from tasks.models import Task


# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "status",
        "assigned_to",
        "created_by",
        "deadline",
        "created_at",
    )
    list_filter = ("status", "deadline")
    search_fields = ("title", "description")
