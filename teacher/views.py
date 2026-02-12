from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from common.models import *
from common.other import check_user_group
from teacher.forms import *


@check_user_group('Teachers')
def teachers_page(request):
    return render(request, 'teachers_page.html', {'user': request.user})

@check_user_group('Teachers')
def all_lessons(request):
    if request.method == "POST":
        form = LessonForm(request.POST)
        # file_form = FileForm(request.POST)

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
    lesson = get_object_or_404(Lesson, id=lesson_id)
    
    if lesson.teacher != request.user:
        messages.error(request, "You do not have permission to view this lesson.")
        return redirect('all_lessons_teacher')

    students_in_school_class = [itm.student for itm in StudentClass.objects.filter(school_class=lesson.school_class)]
    absent_students = [abs.student.id for abs in LessonVisits.objects.filter(lesson=lesson)]
    homeworks = StudentHomework.objects.filter(lesson=lesson)

    grades = Grade.objects.filter(lesson=lesson)
    grades_map = {g.student.id: g.grade for g in grades if g.is_homework == False}

    for student in students_in_school_class:
        student.is_absent = "checked" if student.id in absent_students else ""
        student.grade_value = grades_map.get(student.id, "")

    return render(request, 'one_lesson.html', {'lesson': lesson, 'all_students': students_in_school_class, 'homeworks': homeworks})

@check_user_group('Teachers')
def check_student_absence(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == "POST":
        student_ids = request.POST.getlist('absence_student_ids')

        LessonVisits.objects.filter(lesson=lesson).delete()
        
        for student_id in student_ids:
            student = User.objects.get(id=student_id)
            LessonVisits.objects.create(lesson=lesson, student=student)

        messages.success(request, "Відвідування оновлено успішно.")
        return redirect('one_lesson_teacher', lesson_id=lesson.id)
    
    return redirect('one_lesson_teacher', lesson_id=lesson.id)


@check_user_group('Teachers')
def grade(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    created = False

    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("grade_"):
                student_id = int(key.removeprefix("grade_"))
                student = User.objects.get(id=student_id)
                is_grade = Grade.objects.filter(lesson=lesson, student=student, is_homework=False)

                if not value:
                    Grade.objects.filter(lesson=lesson, student=student).delete()
                    continue

                if is_grade:
                    is_grade.update(grade=value)

                else:
                    new_grade = Grade.objects.create(
                    lesson=lesson,
                    student=student,
                    teacher=request.user,
                    grade=value
                    )

                    created = True

        if created:
            messages.success(request, f"Оцінки виставлено!")
        else:
            messages.success(request, f"Оцінки оновлено!")

    return redirect('one_lesson_teacher', lesson_id=lesson_id)

@check_user_group('Teachers')
def homework(request, lesson_id, homework_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    if request.method == "POST":

        if homework_id:
            student_homework = get_object_or_404(StudentHomework, id=homework_id)
            student = student_homework.student
            
            grade_value = request.POST.get(f'grade_{student.id}')
            
            if grade_value:
                if student_homework.grade_id:
                    student_homework.grade.grade = grade_value
                    student_homework.grade.save()

                else:
                    new_grade = Grade.objects.create(
                        lesson=lesson,
                        student=student,
                        teacher=request.user,
                        grade=grade_value,
                        is_homework=True
                    )

                    student_homework.grade_id = new_grade.id
                    student_homework.save()

                messages.success(request, "Оцінку успішно збережено!")

        return redirect('lesson_homework', lesson_id=lesson_id, homework_id=homework_id)

    return redirect( 'one_lesson_teacher', lesson_id=lesson_id)
