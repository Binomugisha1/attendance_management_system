from django import forms

from .models import (
    Course,
    CourseUnit,
    Lecturer,
    LecturerAttendance,
    Room,
    Student,
    StudentAttendance,
    Timetable,
)


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'


class CourseUnitForm(forms.ModelForm):
    class Meta:
        model = CourseUnit
        fields = '__all__'


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'


class LecturerForm(forms.ModelForm):
    class Meta:
        model = Lecturer
        fields = '__all__'


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = '__all__'


class TimetableForm(forms.ModelForm):
    class Meta:
        model = Timetable
        fields = '__all__'


class StudentAttendanceForm(forms.ModelForm):
    class Meta:
        model = StudentAttendance
        fields = '__all__'


class LecturerAttendanceForm(forms.ModelForm):
    class Meta:
        model = LecturerAttendance
        fields = '__all__'
