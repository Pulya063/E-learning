from django.contrib import admin

from parent.models import Parents

@admin.register(Parents)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'student']

    search_fields = ['user_id']
