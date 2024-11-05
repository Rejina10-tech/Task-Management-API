from django.contrib import admin
from .models import Task


# Register your models here.
admin.site.register(Task)
# admin.site.register(User)


# class TaskAdmin(admin.ModelAdmin):
#     list_display = ['title', 'status', 'priority', 'deadline']
#     list_filter = ['status', 'priority', 'deadline']  # Adds filtering by these fields in the admin
#     search_fields = ['title', 'description']          # Adds search functionality in the
