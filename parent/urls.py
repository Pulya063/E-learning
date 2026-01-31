from django.urls import path

from parent import views

urlpatterns = [
    path('parents', views.parents_page, name='parents_page'),
    path('parents/student/<int:student_id>', views.parents_student_page, name='parents_student_page'),
    path('parents/lesson/<int:lesson_id>', views.parents_lesson_page, name='parents_lesson_page')
]
