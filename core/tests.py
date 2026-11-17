from datetime import time

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase, TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import (
    Course,
    CourseUnit,
    Lecturer,
    Room,
    Student,
    Timetable,
)


class UrlPatternTests(SimpleTestCase):
    def test_create_urls_use_readable_add_paths(self):
        create_paths = {
            'course_create': '/courses/add/',
            'courseunit_create': '/course-units/add/',
            'student_create': '/students/add/',
            'lecturer_create': '/lecturers/add/',
            'room_create': '/rooms/add/',
            'timetable_create': '/timetables/add/',
            'studentattendance_create': '/student-attendance/add/',
            'lecturerattendance_create': '/lecturer-attendance/add/',
        }

        for route_name, expected_path in create_paths.items():
            with self.subTest(route_name=route_name):
                self.assertEqual(reverse(route_name), expected_path)


class DashboardTests(TestCase):
    def test_dashboard_shows_model_counts_and_theme_styles(self):
        user = User.objects.create_user(username='dashboard-user', password='test-password')
        self.client.force_login(user)
        Course.objects.create(
            course_id='CS101',
            course_name='Computer Science',
            faculty='Computing',
            duration=3,
        )

        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['dashboard_cards']), 8)
        self.assertEqual(response.context['dashboard_cards'][0]['count'], 1)
        self.assertEqual(response.context['summary_cards'][0]['count'], 0)
        self.assertEqual(response.context['summary_cards'][2]['count'], 1)
        self.assertContains(response, 'Dashboard')
        self.assertContains(response, 'Manage records')
        self.assertNotContains(response, 'Daily Sales')
        self.assertContains(response, '/static/core/dashboard/bootstrap.min.css')
        self.assertContains(response, '/static/core/dashboard/fonts.min.css')
        self.assertContains(response, '/static/core/dashboard/kaiadmin.min.css')
        self.assertContains(response, 'col-sm-6 col-lg-3')


class CourseCrudTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='tester', password='test-password')
        self.client.force_login(user)
        self.course = Course.objects.create(
            course_id='CS101',
            course_name='Computer Science',
            faculty='Computing',
            duration=3,
        )

    def test_course_crud_pages_use_their_expected_templates(self):
        response = self.client.get(reverse('course_list'))
        self.assertTemplateUsed(response, 'core/course_page.html')
        self.assertContains(response, 'fas fa-pen')
        self.assertContains(response, 'fas fa-trash')

        response = self.client.get(reverse('course_create'))
        self.assertTemplateUsed(response, 'core/shared_form.html')
        response = self.client.post(reverse('course_create'), {
            'course_id': 'IT202',
            'course_name': 'Information Tech',
            'faculty': 'Computing',
            'duration': 4,
        })
        self.assertRedirects(response, reverse('course_list'))
        self.assertTrue(Course.objects.filter(course_id='IT202').exists())

        response = self.client.get(reverse('course_detail', args=[self.course.pk]))
        self.assertTemplateUsed(response, 'core/shared_detail.html')

        response = self.client.get(reverse('course_update', args=[self.course.pk]))
        self.assertTemplateUsed(response, 'core/shared_form.html')
        response = self.client.post(reverse('course_update', args=[self.course.pk]), {
            'course_id': 'CS101',
            'course_name': 'Updated Course',
            'faculty': 'Computing',
            'duration': 3,
        })
        self.assertRedirects(response, reverse('course_list'))
        self.course.refresh_from_db()
        self.assertEqual(self.course.course_name, 'Updated Course')

        response = self.client.get(reverse('course_delete', args=[self.course.pk]))
        self.assertTemplateUsed(response, 'core/shared_confirm_delete.html')
        response = self.client.post(reverse('course_delete', args=[self.course.pk]))
        self.assertRedirects(response, reverse('course_list'))
        self.assertFalse(Course.objects.filter(pk=self.course.pk).exists())


class StudentCrudTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='student-manager', password='test-password')
        self.client.force_login(user)

    def test_created_student_appears_in_student_table(self):
        response = self.client.post(reverse('student_create'), {
            'reg_number': 'STU-001',
            'student_first_name': 'Alex',
            'student_last_name': 'Student',
            'gender': 'F',
            'address': 'Main Street',
            'faculty': 'Computing',
            'course': '',
            'birth_date': '',
            'user': '',
        })

        self.assertRedirects(response, reverse('student_list'))
        self.assertTrue(Student.objects.filter(reg_number='STU-001').exists())

        response = self.client.get(reverse('student_list'))
        self.assertContains(response, 'STU-001')
        self.assertContains(response, 'Alex')

    def test_invalid_student_form_explains_why_it_was_not_saved(self):
        response = self.client.post(reverse('student_create'), {
            'reg_number': '',
            'student_first_name': '',
            'student_last_name': '',
            'gender': '',
            'address': '',
            'faculty': '',
            'course': '',
            'birth_date': '',
            'user': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please correct the following errors:')
        self.assertFalse(Student.objects.exists())


class ExtendedTextLengthTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='records-manager', password='test-password')
        self.client.force_login(user)

    def test_long_student_names_faculty_and_address_are_accepted(self):
        first_name = 'Alexandria' * 5
        last_name = 'Studentlastname' * 4
        faculty = 'Faculty of Agriculture and Environmental Sciences'
        address = ('Main Street, ' * 10).strip()
        response = self.client.post(reverse('student_create'), {
            'reg_number': 'STU-LONG-01',
            'student_first_name': first_name,
            'student_last_name': last_name,
            'gender': 'F',
            'address': address,
            'faculty': faculty,
            'course': '',
            'birth_date': '',
            'user': '',
        })

        self.assertRedirects(response, reverse('student_list'))
        student = Student.objects.get(reg_number='STU-LONG-01')
        self.assertEqual(student.student_first_name, first_name)
        self.assertEqual(student.student_last_name, last_name)
        self.assertEqual(student.faculty, faculty)
        self.assertEqual(student.address, address)

    def test_long_course_and_unit_names_are_accepted(self):
        course_name = ('Advanced International Studies ' * 3).strip()
        faculty = 'Faculty of Agriculture and Environmental Sciences'
        response = self.client.post(reverse('course_create'), {
            'course_id': 'C1001',
            'course_name': course_name,
            'faculty': faculty,
            'duration': 4,
        })
        self.assertRedirects(response, reverse('course_list'))
        course = Course.objects.get(course_id='C1001')
        self.assertEqual(course.course_name, course_name)
        self.assertEqual(course.faculty, faculty)

        unit_name = 'Advanced Applied Computing and Information Systems'
        response = self.client.post(reverse('courseunit_create'), {
            'course_unit_code': 'CU1001',
            'course': course.pk,
            'course_unit_name': unit_name,
            'course_unit_credit': 4,
            'year_of_study': '1',
        })
        self.assertRedirects(response, reverse('courseunit_list'))
        self.assertEqual(CourseUnit.objects.get(pk='CU1001').course_unit_name, unit_name)

    def test_long_lecturer_and_room_text_are_accepted(self):
        lecturer_first_name = 'Alexandria' * 5
        lecturer_last_name = 'Lecturerlastname' * 4
        faculty = 'Faculty of Agriculture and Environmental Sciences'
        address = ('Main Street, ' * 10).strip()
        contact = '+256-700-123-456-789'
        response = self.client.post(reverse('lecturer_create'), {
            'lecturer_id': 'LEC-LONG-01',
            'lecturer_first_name': lecturer_first_name,
            'lecturer_last_name': lecturer_last_name,
            'gender': 'M',
            'address': address,
            'faculty': faculty,
            'contact': contact,
            'user': '',
        })
        self.assertRedirects(response, reverse('lecturer_list'))
        lecturer = Lecturer.objects.get(lecturer_id='LEC-LONG-01')
        self.assertEqual(lecturer.lecturer_first_name, lecturer_first_name)
        self.assertEqual(lecturer.lecturer_last_name, lecturer_last_name)
        self.assertEqual(lecturer.faculty, faculty)
        self.assertEqual(lecturer.contact, contact)

        room_name = 'International Conference and Learning Centre'
        response = self.client.post(reverse('room_create'), {
            'room_id': 'ROOM001',
            'room_name': room_name,
            'capacity': 100,
        })
        self.assertRedirects(response, reverse('room_list'))
        self.assertEqual(Room.objects.get(pk='ROOM001').room_name, room_name)


class TimetableTimeValidationTests(TestCase):
    def setUp(self):
        course = Course.objects.create(
            course_id='CS101',
            course_name='Computer Science',
            faculty='Computing',
            duration=3,
        )
        self.course_unit = CourseUnit.objects.create(
            course_unit_code='CS101A',
            course=course,
            course_unit_name='Introduction to Computing',
            course_unit_credit=3,
            year_of_study='1',
        )
        self.room = Room.objects.create(
            room_id='ROOM001',
            room_name='Lecture Hall',
            capacity=100,
        )

    def _timetable(self, start_time, end_time):
        return Timetable(
            day_of_the_week='Monday',
            course_unit=self.course_unit,
            start_time=start_time,
            end_time=end_time,
            room=self.room,
            semester='1',
            year_of_study='1',
        )

    def test_full_clean_rejects_end_time_before_or_equal_to_start_time(self):
        for start_time, end_time in (
            (time(10, 0), time(9, 59)),
            (time(10, 0), time(10, 0)),
        ):
            with self.subTest(start_time=start_time, end_time=end_time):
                with self.assertRaises(ValidationError) as error:
                    self._timetable(start_time, end_time).full_clean()

                self.assertEqual(
                    error.exception.message_dict['end_time'],
                    ['End time must be after start time.'],
                )

    def test_full_clean_accepts_end_time_after_start_time(self):
        self._timetable(time(9, 0), time(10, 0)).full_clean()

    def test_full_clean_rejects_invalid_semester_and_year_choices(self):
        timetable = self._timetable(time(9, 0), time(10, 0))
        timetable.semester = '3'
        timetable.year_of_study = '5'

        with self.assertRaises(ValidationError) as error:
            timetable.full_clean()

        self.assertIn('semester', error.exception.message_dict)
        self.assertIn('year_of_study', error.exception.message_dict)

    def test_course_unit_rejects_invalid_year_choice(self):
        self.course_unit.year_of_study = '5'

        with self.assertRaises(ValidationError) as error:
            self.course_unit.full_clean()

        self.assertIn('year_of_study', error.exception.message_dict)
