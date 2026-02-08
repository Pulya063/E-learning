from django import forms
from common.models import *

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['subject', 'lesson_name', 'description', 'homework', 'school_class']

class LessonVisitsForm(forms.ModelForm):
    class Meta:
        model = LessonVisits
        fields = ['lesson', 'student']