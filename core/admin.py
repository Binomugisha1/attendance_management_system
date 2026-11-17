
from django.contrib import admin
from .models import (Course, CourseUnit, Student, Lecturer, Room,
                     Timetable, StudentAttendance, LecturerAttendance)

for model in [Course, CourseUnit, Student, Lecturer, Room,
              Timetable, StudentAttendance, LecturerAttendance]:
    admin.site.register(model)