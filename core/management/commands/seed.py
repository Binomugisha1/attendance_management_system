
from django.core.management.base import BaseCommand
from core.models import (Course, CourseUnit, Student, Lecturer, Room,
                         Timetable, StudentAttendance, LecturerAttendance)


class Command(BaseCommand):
    help = "Seed sample data"

    def handle(self, *args, **kwargs):
        c1, _ = Course.objects.get_or_create(course_id='C001',
            defaults={'course_name': 'BIT', 'faculty': 'FOSSA', 'duration': 3})
        c2, _ = Course.objects.get_or_create(course_id='C002',
            defaults={'course_name': 'MNG', 'faculty': 'BUSINESS', 'duration': 3})

        u1, _ = CourseUnit.objects.get_or_create(course_unit_code='C_U001',
            defaults={'course': c1, 'course_unit_name': 'Programming',
                      'course_unit_credit': 3, 'year_of_study': '1'})
        u2, _ = CourseUnit.objects.get_or_create(course_unit_code='C_U002',
            defaults={'course': c1, 'course_unit_name': 'Networking',
                      'course_unit_credit': 4, 'year_of_study': '1'})

        r1, _ = Room.objects.get_or_create(room_id='R001',
            defaults={'room_name': 'LR_17', 'capacity': 50})

        l1, _ = Lecturer.objects.get_or_create(lecturer_id='L001',
            defaults={'lecturer_first_name': 'Musoke', 'lecturer_last_name': 'Peter',
                      'gender': 'M', 'address': 'Jinja', 'faculty': 'Science',
                      'contact': '0788865111'})

        s1, _ = Student.objects.get_or_create(reg_number='224-036215-545',
            defaults={'student_first_name': 'Amad', 'student_last_name': 'Diallo',
                      'gender': 'M', 'address': 'Kibuli', 'faculty': 'Science',
                      'course': c1})

        t1, _ = Timetable.objects.get_or_create(
            day_of_the_week='Monday', course_unit=u1, lecturer=l1,
            start_time='07:30', end_time='10:00', room=r1,
            semester='2', year_of_study='1')

        StudentAttendance.objects.get_or_create(timetable=t1, student=s1,
                                                date_attended='2026-03-21')
        LecturerAttendance.objects.get_or_create(timetable=t1, lecturer=l1,
                                                 date_attended='2026-03-21')
        self.stdout.write(self.style.SUCCESS('Seed data created.'))