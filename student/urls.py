from django.urls import path

from student import views

urlpatterns = [
    path('student', views.student_page, name='student_page'),
    path('student/lessons/', views.all_lessons, name='all_lessons'),
    path('student/lessons/<int:lesson_id>', views.one_lesson, name='one_lesson'),
    path('student/lessons/<int:lesson_id>/submit_homework', views.submit_homework, name='submit_homework')

]
