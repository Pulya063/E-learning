from django.contrib.auth.models import User
from django.shortcuts import render
from common.other import check_user_group
@check_user_group('Students')
def student_page(request):
    student = User.objects.get(id = request.user.id)
    return render(request, 'students_page.html', {'user': student})


def submit_homework(request):
    return ""


def one_lesson(request):
    return ""


def all_lessons(request):
    return ""