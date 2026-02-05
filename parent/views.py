from django.contrib.auth.models import User
from django.shortcuts import render

from common.other import check_user_group


@check_user_group('Parents')
def parent_page(request):
    parent = User.objects.get(id=request.user.id)
    return render(request, 'parents_page.html', {'user': parent})


def parents_student_page(request):
    return ""


def parents_lesson_page(request):
    return ""