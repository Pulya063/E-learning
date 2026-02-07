from django.contrib import admin

from common.models import *


@admin.register(SchoolClass)
class SchoolClassAdmin(admin.ModelAdmin):
    list_display = ['start_year', 'letter']

    search_fields = ['start_year']

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['subject_name']

    search_fields = ['subject_name']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['subject', 'teacher', 'lesson_name', 'lesson_date']

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ['student', 'lesson', 'grade']

    search_fields = ['lesson']

@admin.register(StudentHomework)
class StudentHomeworkAdmin(admin.ModelAdmin):
    list_display = ['student', 'lesson', 'grade']

    search_fields = ['lesson']

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['lesson']

@admin.register(Contacts)
class ContactsAdmin(admin.ModelAdmin):
    list_display = ['phone', 'user']

    search_fields = ['phone']

@admin.register(LessonVisits)
class LessonVisitsAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'student']

    search_fields = ['lesson']