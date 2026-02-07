from django import forms
from common.models import *

class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['subject', 'lesson_name', 'description', 'homework', 'school_class']
        widgets = {
            'lesson_date': forms.DateInput(attrs={'type': 'date'}),
        }


class LessonVisitsForm(forms.ModelForm):
    class Meta:
        model = LessonVisits
        fields = ['lesson', 'student']