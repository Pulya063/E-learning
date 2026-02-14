from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404

from common.models import Grade, Lesson
from common.other import check_user_group
from parent.models import Parents

@check_user_group('Parents')
def parent_page(request):
    parent = User.objects.get(id=request.user.id)
    student = Parents.objects.get(parent=parent)

    return render(request, 'parents_page.html', {'user': parent, 'student': student})

def parents_student_page(request, student_id):
    student = get_object_or_404(User, id=student_id)

    student_grades = Grade.objects.filter(student=student)

    return render(request, 'parents_student_page.html', {'student': student, 'grades': student_grades})

def parents_lesson_page(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    return render(request, 'parents_lesson_page.html', {'lesson': lesson})