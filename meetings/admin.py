from django.contrib import admin
from meetings.models import Meeting
# Register your models here.


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display = ("title", "scheduled_at", "created_by", "created_at")
    list_filter = ("scheduled_at", "created_by")
    search_fields = ("title", "description")
