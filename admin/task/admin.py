# from django import forms
# from django.conf import settings
from django.contrib import admin
from django.forms.widgets import CheckboxSelectMultiple

from easy_thumbnails.widgets import ImageClearableFileInput

from .models import Task, AssignedTask, ChoiceArrayField #, OfferFiler

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    formfield_overrides = {
        'document_template': {'widget': ImageClearableFileInput},
        ChoiceArrayField: {'widget': CheckboxSelectMultiple}
    }
    list_filter = ["task_priority", ]
    list_display = [
        "__str__", "name", "is_listed", 'assignee', "task_priority", "days_to_do", "created_at", "updated_at",
    ]

@admin.register(AssignedTask)
class AssignedTasktAdmin(admin.ModelAdmin):
    list_filter = ["task", "status"]
    list_display = [
        "__str__", "task", "status",
    ]
