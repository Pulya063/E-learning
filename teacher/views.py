from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from common.models import *
from common.other import check_user_group
from teacher.forms import *


@check_user_group('Teachers')
def teachers_page(request):
    teacher = User.objects.filter(id=request.user.id)
    return render(request, 'teachers_page.html', {'user': teacher})

@check_user_group('Teachers')
def all_lessons(request):
    if request.method == "POST":
        form = LessonForm(request.POST)

        if form.is_valid():
            lesson = form.save(commit=False)
            lesson.teacher = request.user
            lesson.save()
            messages.success(request, "Lesson created successfully")
            return redirect("all_lessons_teacher")
        else:
            messages.error(request, "Invalid form data")

    form = LessonForm()
    subjects = Subject.objects.all()
    lessons = Lesson.objects.filter(teacher=request.user).all()

    return render(request, 'lessons.html', {"form": form, "all_teachers_lessons": lessons, "subjects": subjects})


@check_user_group('Teachers')
def one_lesson(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    students_in_school_class = [itm.student for itm in StudentClass.objects.filter(school_class=lesson.school_class)]

    absent_students = [abs.student.id for abs in LessonVisits.objects.filter(lesson=lesson)]

    for student in students_in_school_class:
        student.is_absent = "checked" if student.id in absent_students else ""

    if lesson.teacher != request.user:
        messages.error(request, "You do not have permission to view this lesson.")
        return redirect('all_lessons_teacher')

    return render(request, 'one_lesson.html', {'lesson': lesson, 'all_students': students_in_school_class})

@check_user_group('Teachers')
def check_student_absence(request, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id)
    
    if request.method == "POST":
        student_ids = request.POST.getlist('absence_student_ids')

        LessonVisits.objects.filter(lesson=lesson).delete()
        
        for student_id in student_ids:
            student = User.objects.get(id=student_id)
            absence = LessonVisits.objects.create(lesson=lesson, student=student)
            absence.save()

        messages.success(request, "Відвідування оновлено успішно.")
        return redirect('one_lesson_teacher', lesson_id=lesson.id)
    
    return redirect('one_lesson_teacher', lesson_id=lesson.id)

@check_user_group('Teachers')
def grade(request):
    return render(request, 'grade.html')

@check_user_group('Teachers')
def homework(request):
    return render(request, 'homework.html')
