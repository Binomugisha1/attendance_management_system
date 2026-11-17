
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


SEMESTER_CHOICES = [
    ('1', 'Semester 1'),
    ('2', 'Semester 2'),
]

YEAR_OF_STUDY_CHOICES = [
    ('1', 'Year 1'),
    ('2', 'Year 2'),
    ('3', 'Year 3'),
    ('4', 'Year 4'),
]


class Course(models.Model):
    course_id = models.CharField(max_length=5, unique=True)
    course_name = models.CharField(max_length=100)
    faculty = models.CharField(max_length=100)
    duration = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        ordering = ['course_id']

    def __str__(self):
        return f"{self.course_id} - {self.course_name}"


class CourseUnit(models.Model):
    course_unit_code = models.CharField(max_length=6, primary_key=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='units')
    course_unit_name = models.CharField(max_length=100)
    course_unit_credit = models.PositiveIntegerField()
    year_of_study = models.CharField(
        max_length=1, blank=True, choices=YEAR_OF_STUDY_CHOICES
    )

    def __str__(self):
        return f"{self.course_unit_code} - {self.course_unit_name}"


class Student(models.Model):
    GENDER = [('M', 'Male'), ('F', 'Female')]
    reg_number = models.CharField(max_length=30, unique=True)
    student_first_name = models.CharField(max_length=100)
    student_last_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    address = models.CharField(max_length=255, blank=True)
    faculty = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL,
                               null=True, blank=True, related_name='students')
    birth_date = models.DateField(null=True, blank=True)
    user = models.OneToOneField(User, null=True, blank=True,
                                on_delete=models.SET_NULL,
                                related_name='student_profile')

    def __str__(self):
        return f"{self.reg_number} - {self.student_first_name} {self.student_last_name}"


class Lecturer(models.Model):
    GENDER = [('M', 'Male'), ('F', 'Female')]
    lecturer_id = models.CharField(max_length=30, unique=True)
    lecturer_first_name = models.CharField(max_length=100)
    lecturer_last_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    address = models.CharField(max_length=255, blank=True)
    faculty = models.CharField(max_length=100)
    contact = models.CharField(max_length=25)
    user = models.OneToOneField(User, null=True, blank=True,
                                on_delete=models.SET_NULL,
                                related_name='lecturer_profile')

    def __str__(self):
        return f"{self.lecturer_id} - {self.lecturer_first_name} {self.lecturer_last_name}"


class Room(models.Model):
    room_id = models.CharField(max_length=7, primary_key=True)
    room_name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.room_id} - {self.room_name}"


class Timetable(models.Model):
    DAYS = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
    ]

    timetable_id = models.AutoField(primary_key=True)
    day_of_the_week = models.CharField(max_length=9, choices=DAYS)
    course_unit = models.ForeignKey(
        CourseUnit, on_delete=models.CASCADE, related_name='timetables',
    )
    lecturer = models.ForeignKey(
        Lecturer, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='timetables',
    )
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='timetables',
    )
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    year_of_study = models.CharField(max_length=1, choices=YEAR_OF_STUDY_CHOICES)

    def clean(self):
        super().clean()
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError({
                'end_time': 'End time must be after start time.',
            })

    def __str__(self):
        return (f"{self.day_of_the_week} {self.start_time}-{self.end_time} "
                f"{self.course_unit}")


class StudentAttendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE,
                                  related_name='student_attendances')
    student = models.ForeignKey(Student, on_delete=models.CASCADE,
                                related_name='attendances')
    date_attended = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('timetable', 'student', 'date_attended')

    def __str__(self):
        return f"{self.student.reg_number} @ {self.timetable} on {self.date_attended}"


class LecturerAttendance(models.Model):
    attendance_id = models.AutoField(primary_key=True)
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE,
                                  related_name='lecturer_attendances')
    lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE,
                                 related_name='attendances')
    date_attended = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('timetable', 'lecturer', 'date_attended')

    def __str__(self):
        return f"{self.lecturer.lecturer_id} @ {self.timetable} on {self.date_attended}"