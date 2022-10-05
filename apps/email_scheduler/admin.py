from django.contrib import admin
from .models import EmailScheduler, EmailSchedulerLogs
from durationwidget.widgets import TimeDurationWidget
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.forms import Textarea


# Register your models here.


@admin.register(EmailScheduler)
class EmailSchedulerAdmin(admin.ModelAdmin):
    formfield_overrides = {
        ArrayField: {"widget": Textarea(attrs={"rows": 2, "cols": 60})},
        models.CharField: {"widget": Textarea(attrs={"rows": 2, "cols": 80})},
    }
    readonly_fields = [
        "email_last_sent_at",
        "task_status",
        "email_send_count",
        "task_failed_count",
        "task_failure_info",
    ]


@admin.register(EmailSchedulerLogs)
class EmailSchedulerLogsAdmin(admin.ModelAdmin):
    def has_add_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
