import datetime

from django.conf import settings
from django.db import models
from django.db.models import ForeignKey
from django.db.models.fields import DateField, CharField, TextField, FilePathField


class SchoolClass(models.Model):
    start_year = DateField()
    letter = CharField(max_length=1)

    def date_validator(self):
        if type(self.start_year) != datetime.date:
            self.start_year = datetime.date(int(self.start_year.year), 8, 1)
            return self.start_year
        else:
            return self.start_year


    def __str__(self):
        return f"{self.start_year} {self.letter}"


class Subject(models.Model):
    subject_name = CharField(max_length=70)

    def __str__(self):
        return f"{self.subject_name}"


class Lesson(models.Model):
    subject = ForeignKey(Subject, on_delete=models.CASCADE)
    lesson_date = DateField(default=datetime.date.today())
    teacher = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson_name = CharField(max_length=70)
    description = TextField(max_length=1000)
    homework = CharField(max_length=70)
    school_class = ForeignKey(SchoolClass, on_delete=models.CASCADE)

    def __str__(self):
        return f"lesson_name: {self.lesson_name}, subject: {self.subject}, teacher: {self.teacher}, school_class: {self.school_class}"

class StudentClass(models.Model):
    school_class = ForeignKey(SchoolClass, on_delete=models.CASCADE)
    student = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"school_class: {self.school_class}, student: {self.student}"


class Grade(models.Model):
    student = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_grade")
    lesson = ForeignKey(Lesson, on_delete=models.CASCADE, related_name="lesson_grade")
    teacher = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="teacher_grade")
    grade = CharField(max_length=1)

    def __str__(self):
        return f"student: {self.student}, lesson: {self.lesson}, grade: {self.grade}"

class StudentHomework(models.Model):
    student = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = ForeignKey(Lesson, on_delete=models.CASCADE)
    text_data = TextField(max_length=1000)
    grade = ForeignKey(Grade, on_delete=models.CASCADE)

    def __str__(self):
        return f"student: {self.student}, lesson: {self.lesson}, grade: {self.grade}"

class File(models.Model):
    lesson = ForeignKey(Lesson, on_delete=models.CASCADE)
    file_path = FilePathField()

    def __str__(self):
        return f"file_path: {self.file_path}"

class Contacts(models.Model):
    phone = CharField(max_length=11)
    user = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"phone: {self.phone}, user: {self.user}"

class LessonVisits(models.Model):
    lesson = ForeignKey(Lesson, on_delete=models.CASCADE)
    student = ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"lesson: {self.lesson}, student: {self.student}"
