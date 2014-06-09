from django.contrib import admin

from .models import Object


class ObjectAdmin(admin.ModelAdmin):
    list_display = ('name','slug','account')
    search_fields = ['id', 'name','slug', 'account']
admin.site.register(Object, ObjectAdmin)
