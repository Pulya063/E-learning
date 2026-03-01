from django.test import TestCase, Client
from django.urls import reverse

from common.models import Lesson, Grade, StudentHomework


class TeacherTest(TestCase):
    fixtures = ["fixture"]

    def setUp(self):
        client = Client()
        client.login(username="teacher", password="1111")
        self.client = client

    def test_teachers_page(self):
        response = self.client.get('/teachers/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teachers_page.html')

    def test_teacher_all_lessons(self):
        response = self.client.get('/teachers/lessons')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teacher_lessons.html')

    def test_create_lesson(self):
        response = self.client.post('/teachers/lessons', {
            'subject': 1,
            'lesson_name': 'Math Lesson',
            'teacher': 17,
            'school_class': 1,
            'date': '2024-06-01',
            'homework': 'Read chapter 1',
            'description': 'Introduction to the subject'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/teachers/lessons')
        created_lesson = Lesson.objects.get(lesson_name='Math Lesson')
        self.assertIsNotNone(created_lesson)
        self.assertEqual(created_lesson.school_class.pk, 1)

    def test_one_lesson(self):
        response = self.client.get('/teachers/lesson/1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'teacher_one_lesson.html')

    def test_one_lesson_update(self):
        response = self.client.post('/teachers/lesson/1', {
            'subject': 1,
            'lesson_name': 'Updated Math Lesson',
            'teacher': 17,
            'school_class': 1,
            'date': '2024-06-01',
            'homework': 'Read chapter 1',
            'description': 'Introduction to the subject'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/teachers/lesson/1')
        updated_lesson = Lesson.objects.get(pk=1)
        self.assertEqual(updated_lesson.lesson_name, 'Updated Math Lesson')

    def test_show_student_absence(self):
        response = self.client.get('/teachers/lesson/1/absence')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/teachers/lesson/1')

    def test_check_student_absence(self):
        response = self.client.post('/teachers/lesson/1/absence',{'student_id': [1]})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/teachers/lesson/1')

    def test_get_grades(self):
        response = self.client.get('/teachers/lesson/1/grade')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/teachers/lesson/1')

    def test_create_grade(self):
        response = self.client.post('/teachers/lesson/1/grade', {
            f'grade_{16}': 9,
            'student': 16,
            'teacher': 17,
            'lesson': 1,
            'is_homework': False
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/teachers/lesson/1')

    def test_update_grade(self):
        test_lesson = Lesson.objects.get(pk=1)

        self.assertIsNotNone(test_lesson)

        response = self.client.post('/teachers/lesson/1/grade', {
            f'grade_{16}': 9,
            'student': 16,
            'teacher': 17,
            'lesson': 1,
            'is_homework': False
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Grade.objects.filter(lesson=test_lesson, is_homework=False, student_id=16).count(), 1)
        self.assertEqual(Grade.objects.get(lesson=test_lesson, is_homework=False, student_id=16).grade, '9')
        self.assertRedirects(response, '/teachers/lesson/1')

    def test_delete_grade_on_empty_value(self):
        test_lesson = Lesson.objects.get(pk=1)

        self.assertIsNotNone(test_lesson)

        response = self.client.post('/teachers/lesson/1/grade', {
            f'grade_{16}': '',
            'student': 16,
            'teacher': 17,
            'lesson': 1,
            'is_homework': False
        })

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Grade.objects.filter(lesson=test_lesson, student=16).exists())

    def test_set_homework_grade(self):
        student = StudentHomework.objects.get(pk=10)

        response = self.client.post(f'/teachers/lesson/1/homeworks/{student.id}', {
            f'grade_{student.id}': 8,
            'student': student.id,
            'teacher': 17,
            'lesson': 1,
            'is_homework': True
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            reverse('lesson_homework', args=[1, student.id])
        )

    def test_get_homework_page(self):
        student = StudentHomework.objects.get(pk=10)
        self.assertIsNotNone(student)

        response = self.client.get(f'/teachers/lesson/1/homeworks/{student.id}')
        self.assertEqual(response.status_code, 302)