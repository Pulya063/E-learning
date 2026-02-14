from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

from common.models import Lesson, StudentClass, Grade, StudentHomework
from common.other import check_user_group
from student.forms import HomeworkForm
from teacher.forms import LessonForm


@check_user_group('Students')
def student_page(request):
    student = User.objects.get(id = request.user.id)
    return render(request, 'students_page.html', {'user': student})

@check_user_group('Students')
def submit_homework(request, lesson_id):
    if request.method == "POST":
        is_homework = StudentHomework.objects.filter(lesson=lesson_id, student=request.user).first()

        if is_homework:
            form = HomeworkForm(instance=is_homework)
            if form.is_valid():
                form.save()

        else:
            form = HomeworkForm(request.POST)

            if form.is_valid():
                homework = form.save(commit=False)
                homework.student = request.user
                homework.lesson = get_object_or_404(Lesson, id=lesson_id)
                homework.save()

    return redirect('one_lesson', lesson_id=lesson_id)

@check_user_group('Students')
def one_lesson(request, lesson_id):
    one_lesson = get_object_or_404(Lesson, id=lesson_id)
    homework_form = HomeworkForm()
    homework_grade = Grade.objects.filter(lesson=one_lesson, student=request.user, is_homework=True).first()
    return render(request, 'students_one_lesson.html', {'lesson': one_lesson, 'homework_form': homework_form, "grade": homework_grade})

@check_user_group('Students')
def all_lessons(request):
    student_school_class = StudentClass.objects.get(student=request.user).school_class
    lessons = Lesson.objects.filter(school_class=student_school_class)
    return render(request, 'students_lessons.html', {"all_lessons": lessons})