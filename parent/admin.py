from django.contrib import admin

from parent.models import Parents

@admin.register(Parents)
class ParentAdmin(admin.ModelAdmin):
    list_display = ['parent', 'student']

    search_fields = ['parent__username', 'student__username']
