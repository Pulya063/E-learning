from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from common.models import *
from common.other import check_user_group
from teacher.forms import *


@check_user_group('Teachers')
def teachers_page(request):
    teacher = User.objects.get(id=request.user.id)
    return render(request, 'teachers_page.html', {'user': teacher})

@check_user_group('Teachers')
def all_lessons(request):
    if request.method == "POST":
        lesson = LessonForm(request.POST)

        if not lesson.is_valid():
            messages.error(request, "Invalid credentials")
            return redirect('register')

        lesson.save()
        messages.success(request, "You are registered")
        return redirect("login")

    lesson = LessonForm()
    return render(request, 'create_lesson.html', {"form": lesson})


@check_user_group('Teachers')
def one_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    return ''
@check_user_group('Teachers')
def check_student_absence(request):
    return ""

@check_user_group('Teachers')
def grade(request):
    return ""

@check_user_group('Teachers')
def homework(request):
    return ""