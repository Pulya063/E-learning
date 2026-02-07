from django.conf import settings
from django.db import models
from django.db.models import ForeignKey


class Parents(models.Model):
    user_id = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parent_user')
    student = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parent_student')