# from django import forms
# from django.conf import settings
from django.contrib import admin
# from django.utils.html import mark_safe

from easy_thumbnails.widgets import ImageClearableFileInput

from .models import Task, AssignedTask #, OfferFiler

# class offer_filer_inline(admin.TabularInline):
#     model = OfferFiler
#     extra = 1

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # def formfield_for_foreignkey(self, db_field, request, **kwargs):
    #     if db_field.name == 'user':
    #         kwargs['initial'] = request.user.id
    #     return super(TaskAdmin, self).formfield_for_foreignkey(
    #         db_field, request, **kwargs
    #     )
    # def get_thumbnail(self, obj):
    #     if obj.image:
    #         try:
    #             return mark_safe('<img src="%s/%s"/>' % (settings.MEDIA_URL, obj.image.get_thumbnail({
    #                 'size': (80, 80) }
    #             )))
    #         except:
    #             pass
    #     return ''
    
    # get_thumbnail.short_description = 'Thumbnail'
    # get_thumbnail.allow_tags = True

    formfield_overrides = {
        'document_template': {'widget': ImageClearableFileInput},
    }
    list_filter = ["status", ]
    list_display = [
        "__str__", "name", "status", "task_priority", "days_to_do", "created_at", "updated_at",
    ]

    # inlines = (offer_filer_inline,)
    # prepopulated_fields = {"slug": ("name", )}

@admin.register(AssignedTask)
class AssignedTasktAdmin(admin.ModelAdmin):
    list_filter = ["task", "user", "completed"]
    list_display = [
        "id", "task", "user", "completed",
    ]
