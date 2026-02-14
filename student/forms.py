from django import forms
from common.models import *

class HomeworkForm(forms.ModelForm):
    class Meta:
        model = StudentHomework
        fields = ['text_data']