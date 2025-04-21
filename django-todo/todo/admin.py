from django.contrib import admin
from .models import Task, Category, Tag

class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'due_date', 'priority', 'complete')
    list_filter = ('complete', 'priority', 'category')
    search_fields = ('title', 'description')
    filter_horizontal = ('tags',)

# Register models only once
admin.site.register(Task, TaskAdmin)
admin.site.register(Category)
admin.site.register(Tag)