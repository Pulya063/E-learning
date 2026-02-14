from django import forms
from common.models import *

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['subject', 'lesson_name', 'description', 'homework', 'school_class']
        exclude = []

class LessonVisitsForm(forms.ModelForm):
    class Meta:
        model = LessonVisits
        fields = ['lesson', 'student']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'lesson', 'teacher', 'grade']

#
# class FileForm(forms.ModelForm):
#     class Meta:
#         model = File
#         fields = ['file_path', 'lesson']