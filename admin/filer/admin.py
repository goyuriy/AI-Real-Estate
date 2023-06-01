from django.contrib import admin

from .models import Filer

@admin.register(Filer)
class FilerAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'user':
            kwargs['initial'] = request.user.id
        return super(FilerAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs
        )

    list_display = [
        "__str__", "filename", "name", "url",
    ]

    def save_model(self, request, obj, form, change):
        f = request.FILES.get('url')
        if f:
            obj.filename = f.name.split('.')[0]
            obj.mime = f.content_type

        return super().save_model(request, obj, form, change)
