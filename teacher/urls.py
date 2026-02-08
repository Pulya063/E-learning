from django.urls import path

from teacher import views

urlpatterns = [
    path('teachers', views.teachers_page, name='teacher_page'),
    path('teachers/lessons', views.all_lessons, name='all_lessons_teacher'),
    path('teachers/lesson/<int:lesson_id>', views.one_lesson, name='one_lesson_teacher'),
    path('teachers/lesson/<int:lesson_id>/absence', views.check_student_absence, name='check_student_absence'),
    path('teachers/lesson/<int:lesson_id>/grade', views.grade, name='grade'),
    path('teachers/lesson/<int:lesson_id>/homework/<int:homework_id>', views.homework, name='create_homework')
]
