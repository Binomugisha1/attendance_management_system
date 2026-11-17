from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),

    path('courses/', views.course_list, name='course_list'),
    path('courses/add/', views.course_create, name='course_create'),
    path('courses/<str:pk>/', views.course_detail, name='course_detail'),
    path('courses/<str:pk>/update/', views.course_update, name='course_update'),
    path('courses/<str:pk>/delete/', views.course_delete, name='course_delete'),

    path('course-units/', views.courseunit_list, name='courseunit_list'),
    path('course-units/add/', views.courseunit_create, name='courseunit_create'),
    path('course-units/<str:pk>/', views.courseunit_detail, name='courseunit_detail'),
    path('course-units/<str:pk>/update/', views.courseunit_update, name='courseunit_update'),
    path('course-units/<str:pk>/delete/', views.courseunit_delete, name='courseunit_delete'),

    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.student_create, name='student_create'),
    path('students/<str:pk>/', views.student_detail, name='student_detail'),
    path('students/<str:pk>/update/', views.student_update, name='student_update'),
    path('students/<str:pk>/delete/', views.student_delete, name='student_delete'),

    path('lecturers/', views.lecturer_list, name='lecturer_list'),
    path('lecturers/add/', views.lecturer_create, name='lecturer_create'),
    path('lecturers/<str:pk>/', views.lecturer_detail, name='lecturer_detail'),
    path('lecturers/<str:pk>/update/', views.lecturer_update, name='lecturer_update'),
    path('lecturers/<str:pk>/delete/', views.lecturer_delete, name='lecturer_delete'),

    path('rooms/', views.room_list, name='room_list'),
    path('rooms/add/', views.room_create, name='room_create'),
    path('rooms/<str:pk>/', views.room_detail, name='room_detail'),
    path('rooms/<str:pk>/update/', views.room_update, name='room_update'),
    path('rooms/<str:pk>/delete/', views.room_delete, name='room_delete'),

    path('timetables/', views.timetable_list, name='timetable_list'),
    path('timetables/add/', views.timetable_create, name='timetable_create'),
    path('timetables/<str:pk>/', views.timetable_detail, name='timetable_detail'),
    path('timetables/<str:pk>/update/', views.timetable_update, name='timetable_update'),
    path('timetables/<str:pk>/delete/', views.timetable_delete, name='timetable_delete'),

    path('student-attendance/', views.studentattendance_list, name='studentattendance_list'),
    path('student-attendance/add/', views.studentattendance_create, name='studentattendance_create'),
    path('student-attendance/<str:pk>/', views.studentattendance_detail, name='studentattendance_detail'),
    path('student-attendance/<str:pk>/update/', views.studentattendance_update, name='studentattendance_update'),
    path('student-attendance/<str:pk>/delete/', views.studentattendance_delete, name='studentattendance_delete'),

    path('lecturer-attendance/', views.lecturerattendance_list, name='lecturerattendance_list'),
    path('lecturer-attendance/add/', views.lecturerattendance_create, name='lecturerattendance_create'),
    path('lecturer-attendance/<str:pk>/', views.lecturerattendance_detail, name='lecturerattendance_detail'),
    path('lecturer-attendance/<str:pk>/update/', views.lecturerattendance_update, name='lecturerattendance_update'),
    path('lecturer-attendance/<str:pk>/delete/', views.lecturerattendance_delete, name='lecturerattendance_delete'),
]
