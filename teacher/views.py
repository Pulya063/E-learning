from django.contrib.auth.models import User
from django.shortcuts import render

from common.other import check_user_group


@check_user_group('Teachers')
def teachers_page(request):
    teacher = User.objects.get(id=request.user.id)
    return render(request, 'teachers_page.html', {'user': teacher})


def all_lessons(request):
    return ""


def one_lesson(request):
    return ""


def check_student_absence(request):
    return ""


def grade(request):
    return ""


def homework(request):
    return ""