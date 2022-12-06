from django.contrib import admin
from project.models import Apps

# Register your models here.
class AppsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image', 'updated_date', 'created_date']
    ordering = ['-created_date']
admin.site.register(Apps, AppsAdmin)