from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CourseForm,
    CourseUnitForm,
    LecturerAttendanceForm,
    LecturerForm,
    RoomForm,
    StudentAttendanceForm,
    StudentForm,
    TimetableForm,
)
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


@login_required
def home_page(request):
    course_count = Course.objects.count()
    course_unit_count = CourseUnit.objects.count()
    student_count = Student.objects.count()
    lecturer_count = Lecturer.objects.count()
    room_count = Room.objects.count()
    timetable_count = Timetable.objects.count()
    student_attendance_count = StudentAttendance.objects.count()
    lecturer_attendance_count = LecturerAttendance.objects.count()

    dashboard_cards = [
        {
            'label': 'Courses',
            'count': course_count,
            'list_url': 'course_list',
            'create_url': 'course_create',
            'icon': 'fas fa-book',
            'color': 'primary',
        },
        {
            'label': 'Course Units',
            'count': course_unit_count,
            'list_url': 'courseunit_list',
            'create_url': 'courseunit_create',
            'icon': 'fas fa-book-open',
            'color': 'info',
        },
        {
            'label': 'Students',
            'count': student_count,
            'list_url': 'student_list',
            'create_url': 'student_create',
            'icon': 'fas fa-user-graduate',
            'color': 'success',
        },
        {
            'label': 'Lecturers',
            'count': lecturer_count,
            'list_url': 'lecturer_list',
            'create_url': 'lecturer_create',
            'icon': 'fas fa-chalkboard-teacher',
            'color': 'secondary',
        },
        {
            'label': 'Rooms',
            'count': room_count,
            'list_url': 'room_list',
            'create_url': 'room_create',
            'icon': 'fas fa-door-open',
            'color': 'warning',
        },
        {
            'label': 'Timetable',
            'count': timetable_count,
            'list_url': 'timetable_list',
            'create_url': 'timetable_create',
            'icon': 'fas fa-calendar-alt',
            'color': 'danger',
        },
        {
            'label': 'Student Attendance',
            'count': student_attendance_count,
            'list_url': 'studentattendance_list',
            'create_url': 'studentattendance_create',
            'icon': 'fas fa-user-check',
            'color': 'info',
        },
        {
            'label': 'Lecturer Attendance',
            'count': lecturer_attendance_count,
            'list_url': 'lecturerattendance_list',
            'create_url': 'lecturerattendance_create',
            'icon': 'fas fa-clipboard-check',
            'color': 'success',
        },
    ]
    summary_cards = [
        {
            'label': 'Students',
            'count': student_count,
            'icon': 'fas fa-user-graduate',
            'color': 'primary',
        },
        {
            'label': 'Lecturers',
            'count': lecturer_count,
            'icon': 'fas fa-chalkboard-teacher',
            'color': 'info',
        },
        {
            'label': 'Courses',
            'count': course_count,
            'icon': 'fas fa-book',
            'color': 'success',
        },
        {
            'label': 'Attendance records',
            'count': student_attendance_count + lecturer_attendance_count,
            'icon': 'fas fa-clipboard-check',
            'color': 'secondary',
        },
    ]
    context = {
        'dashboard_cards': dashboard_cards,
        'summary_cards': summary_cards,
        'total_records': (
            course_count
            + course_unit_count
            + student_count
            + lecturer_count
            + room_count
            + timetable_count
            + student_attendance_count
            + lecturer_attendance_count
        ),
    }
    return render(request, 'core/home_page.html', context)


@login_required
def course_list(request):
    page_obj = Paginator(Course.objects.all(), 20).get_page(request.GET.get('page'))
    return render(request, 'core/course_page.html', {
        'model_verbose': 'Courses',
        'model_name': 'course',
        'fields': list(Course._meta.fields),
        'object_list': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    return render(request, 'core/shared_detail.html', {
        'model_verbose': 'Courses',
        'model_name': 'course',
        'fields': list(Course._meta.fields),
        'object': course,
    })


@login_required
def course_create(request):
    form = CourseForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('course_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Courses',
        'model_name': 'course',
        'fields': list(Course._meta.fields),
        'form': form,
        'object': None,
    })


@login_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
        instance=course,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('course_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Courses',
        'model_name': 'course',
        'fields': list(Course._meta.fields),
        'form': form,
        'object': course,
    })


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('course_list')
    return render(request, 'core/shared_confirm_delete.html', {
        'model_verbose': 'Courses',
        'model_name': 'course',
        'fields': list(Course._meta.fields),
        'object': course,
    })


@login_required
def courseunit_list(request):
    page_obj = Paginator(CourseUnit.objects.all(), 20).get_page(request.GET.get('page'))
    return render(request, 'core/course_unit_page.html', {
        'model_verbose': 'Course Units',
        'model_name': 'courseunit',
        'fields': list(CourseUnit._meta.fields),
        'object_list': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })


@login_required
def courseunit_detail(request, pk):
    course_unit = get_object_or_404(CourseUnit, pk=pk)
    return render(request, 'core/shared_detail.html', {
        'model_verbose': 'Course Units',
        'model_name': 'courseunit',
        'fields': list(CourseUnit._meta.fields),
        'object': course_unit,
    })


@login_required
def courseunit_create(request):
    form = CourseUnitForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('courseunit_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Course Units',
        'model_name': 'courseunit',
        'fields': list(CourseUnit._meta.fields),
        'form': form,
        'object': None,
    })


@login_required
def courseunit_update(request, pk):
    course_unit = get_object_or_404(CourseUnit, pk=pk)
    form = CourseUnitForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
        instance=course_unit,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('courseunit_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Course Units',
        'model_name': 'courseunit',
        'fields': list(CourseUnit._meta.fields),
        'form': form,
        'object': course_unit,
    })


@login_required
def courseunit_delete(request, pk):
    course_unit = get_object_or_404(CourseUnit, pk=pk)
    if request.method == 'POST':
        course_unit.delete()
        return redirect('courseunit_list')
    return render(request, 'core/shared_confirm_delete.html', {
        'model_verbose': 'Course Units',
        'model_name': 'courseunit',
        'fields': list(CourseUnit._meta.fields),
        'object': course_unit,
    })


@login_required
def student_list(request):
    page_obj = Paginator(Student.objects.all(), 20).get_page(request.GET.get('page'))
    return render(request, 'core/student_page.html', {
        'model_verbose': 'Students',
        'model_name': 'student',
        'fields': list(Student._meta.fields),
        'object_list': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })


@login_required
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'core/shared_detail.html', {
        'model_verbose': 'Students',
        'model_name': 'student',
        'fields': list(Student._meta.fields),
        'object': student,
    })


@login_required
def student_create(request):
    form = StudentForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Students',
        'model_name': 'student',
        'fields': list(Student._meta.fields),
        'form': form,
        'object': None,
    })


@login_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
        instance=student,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Students',
        'model_name': 'student',
        'fields': list(Student._meta.fields),
        'form': form,
        'object': student,
    })


@login_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('student_list')
    return render(request, 'core/shared_confirm_delete.html', {
        'model_verbose': 'Students',
        'model_name': 'student',
        'fields': list(Student._meta.fields),
        'object': student,
    })


@login_required
def lecturer_list(request):
    page_obj = Paginator(Lecturer.objects.all(), 20).get_page(request.GET.get('page'))
    return render(request, 'core/lecturer_page.html', {
        'model_verbose': 'Lecturers',
        'model_name': 'lecturer',
        'fields': list(Lecturer._meta.fields),
        'object_list': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })


@login_required
def lecturer_detail(request, pk):
    lecturer = get_object_or_404(Lecturer, pk=pk)
    return render(request, 'core/shared_detail.html', {
        'model_verbose': 'Lecturers',
        'model_name': 'lecturer',
        'fields': list(Lecturer._meta.fields),
        'object': lecturer,
    })


@login_required
def lecturer_create(request):
    form = LecturerForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lecturer_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Lecturers',
        'model_name': 'lecturer',
        'fields': list(Lecturer._meta.fields),
        'form': form,
        'object': None,
    })


@login_required
def lecturer_update(request, pk):
    lecturer = get_object_or_404(Lecturer, pk=pk)
    form = LecturerForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
        instance=lecturer,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lecturer_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Lecturers',
        'model_name': 'lecturer',
        'fields': list(Lecturer._meta.fields),
        'form': form,
        'object': lecturer,
    })


@login_required
def lecturer_delete(request, pk):
    lecturer = get_object_or_404(Lecturer, pk=pk)
    if request.method == 'POST':
        lecturer.delete()
        return redirect('lecturer_list')
    return render(request, 'core/shared_confirm_delete.html', {
        'model_verbose': 'Lecturers',
        'model_name': 'lecturer',
        'fields': list(Lecturer._meta.fields),
        'object': lecturer,
    })


@login_required
def room_list(request):
    page_obj = Paginator(Room.objects.all(), 20).get_page(
        request.GET.get('page')
    )
    return render(request, 'core/room_page.html', {
        'model_verbose': 'Rooms',
        'model_name': 'room',
        'fields': list(Room._meta.fields),
        'object_list': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })


@login_required
def room_detail(request, pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'core/shared_detail.html', {
        'model_verbose': 'Rooms',
        'model_name': 'room',
        'fields': list(Room._meta.fields),
        'object': room,
    })


@login_required
def room_create(request):
    form = RoomForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('room_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Rooms',
        'model_name': 'room',
        'fields': list(Room._meta.fields),
        'form': form,
        'object': None,
    })


@login_required
def room_update(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
        instance=room,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('room_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Rooms',
        'model_name': 'room',
        'fields': list(Room._meta.fields),
        'form': form,
        'object': room,
    })


@login_required
def room_delete(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('room_list')
    return render(request, 'core/shared_confirm_delete.html', {
        'model_verbose': 'Rooms',
        'model_name': 'room',
        'fields': list(Room._meta.fields),
        'object': room,
    })


@login_required
def timetable_list(request):
    page_obj = Paginator(Timetable.objects.all(), 20).get_page(request.GET.get('page'))
    return render(request, 'core/timetable_page.html', {
        'model_verbose': 'Timetable',
        'model_name': 'timetable',
        'fields': list(Timetable._meta.fields),
        'object_list': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })


@login_required
def timetable_detail(request, pk):
    timetable = get_object_or_404(Timetable, pk=pk)
    return render(request, 'core/shared_detail.html', {
        'model_verbose': 'Timetable',
        'model_name': 'timetable',
        'fields': list(Timetable._meta.fields),
        'object': timetable,
    })


@login_required
def timetable_create(request):
    form = TimetableForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('timetable_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Timetable',
        'model_name': 'timetable',
        'fields': list(Timetable._meta.fields),
        'form': form,
        'object': None,
    })


@login_required
def timetable_update(request, pk):
    timetable = get_object_or_404(Timetable, pk=pk)
    form = TimetableForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
        instance=timetable,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('timetable_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Timetable',
        'model_name': 'timetable',
        'fields': list(Timetable._meta.fields),
        'form': form,
        'object': timetable,
    })


@login_required
def timetable_delete(request, pk):
    timetable = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        timetable.delete()
        return redirect('timetable_list')
    return render(request, 'core/shared_confirm_delete.html', {
        'model_verbose': 'Timetable',
        'model_name': 'timetable',
        'fields': list(Timetable._meta.fields),
        'object': timetable,
    })


@login_required
def studentattendance_list(request):
    page_obj = Paginator(StudentAttendance.objects.all(), 20).get_page(
        request.GET.get('page')
    )
    return render(request, 'core/student_attendance_page.html', {
        'model_verbose': 'Student Attendance',
        'model_name': 'studentattendance',
        'fields': list(StudentAttendance._meta.fields),
        'object_list': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })


@login_required
def studentattendance_detail(request, pk):
    attendance = get_object_or_404(StudentAttendance, pk=pk)
    return render(request, 'core/shared_detail.html', {
        'model_verbose': 'Student Attendance',
        'model_name': 'studentattendance',
        'fields': list(StudentAttendance._meta.fields),
        'object': attendance,
    })


@login_required
def studentattendance_create(request):
    form = StudentAttendanceForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('studentattendance_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Student Attendance',
        'model_name': 'studentattendance',
        'fields': list(StudentAttendance._meta.fields),
        'form': form,
        'object': None,
    })


@login_required
def studentattendance_update(request, pk):
    attendance = get_object_or_404(StudentAttendance, pk=pk)
    form = StudentAttendanceForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
        instance=attendance,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('studentattendance_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Student Attendance',
        'model_name': 'studentattendance',
        'fields': list(StudentAttendance._meta.fields),
        'form': form,
        'object': attendance,
    })


@login_required
def studentattendance_delete(request, pk):
    attendance = get_object_or_404(StudentAttendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        return redirect('studentattendance_list')
    return render(request, 'core/shared_confirm_delete.html', {
        'model_verbose': 'Student Attendance',
        'model_name': 'studentattendance',
        'fields': list(StudentAttendance._meta.fields),
        'object': attendance,
    })


@login_required
def lecturerattendance_list(request):
    page_obj = Paginator(LecturerAttendance.objects.all(), 20).get_page(
        request.GET.get('page')
    )
    return render(request, 'core/lecturer_attendance_page.html', {
        'model_verbose': 'Lecturer Attendance',
        'model_name': 'lecturerattendance',
        'fields': list(LecturerAttendance._meta.fields),
        'object_list': page_obj.object_list,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    })


@login_required
def lecturerattendance_detail(request, pk):
    attendance = get_object_or_404(LecturerAttendance, pk=pk)
    return render(request, 'core/shared_detail.html', {
        'model_verbose': 'Lecturer Attendance',
        'model_name': 'lecturerattendance',
        'fields': list(LecturerAttendance._meta.fields),
        'object': attendance,
    })


@login_required
def lecturerattendance_create(request):
    form = LecturerAttendanceForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lecturerattendance_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Lecturer Attendance',
        'model_name': 'lecturerattendance',
        'fields': list(LecturerAttendance._meta.fields),
        'form': form,
        'object': None,
    })


@login_required
def lecturerattendance_update(request, pk):
    attendance = get_object_or_404(LecturerAttendance, pk=pk)
    form = LecturerAttendanceForm(
        request.POST if request.method == 'POST' else None,
        request.FILES if request.method == 'POST' else None,
        instance=attendance,
    )
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lecturerattendance_list')
    return render(request, 'core/shared_form.html', {
        'model_verbose': 'Lecturer Attendance',
        'model_name': 'lecturerattendance',
        'fields': list(LecturerAttendance._meta.fields),
        'form': form,
        'object': attendance,
    })


@login_required
def lecturerattendance_delete(request, pk):
    attendance = get_object_or_404(LecturerAttendance, pk=pk)
    if request.method == 'POST':
        attendance.delete()
        return redirect('lecturerattendance_list')
    return render(request, 'core/shared_confirm_delete.html', {
        'model_verbose': 'Lecturer Attendance',
        'model_name': 'lecturerattendance',
        'fields': list(LecturerAttendance._meta.fields),
        'object': attendance,
    })
