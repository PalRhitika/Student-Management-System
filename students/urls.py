from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Students
    path("students/", views.StudentListView.as_view(), name="student_list"),
    path("students/create/", views.StudentCreateView.as_view(), name="student_create"),
    path("students/<int:pk>/", views.StudentDetailView.as_view(), name="student_detail"),
    path("students/<int:pk>/edit/", views.StudentUpdateView.as_view(), name="student_edit"),
    path("students/<int:pk>/delete/", views.StudentDeleteView.as_view(), name="student_delete"),

    # Courses
    path("courses/", views.CourseListView.as_view(), name="course_list"),
    path("courses/create/", views.CourseCreateView.as_view(), name="course_create"),
    path("courses/<int:pk>/", views.CourseDetailView.as_view(), name="course_detail"),
    path("courses/<int:pk>/edit/", views.CourseUpdateView.as_view(), name="course_edit"),
    path("courses/<int:pk>/delete/", views.CourseDeleteView.as_view(), name="course_delete"),

    # Instructors
    path("instructors/", views.InstructorListView.as_view(), name="instructor_list"),
    path("instructors/create/", views.InstructorCreateView.as_view(), name="instructor_create"),
    path("instructors/<int:pk>/", views.InstructorDetailView.as_view(), name="instructor_detail"),
    path("instructors/<int:pk>/edit/", views.InstructorUpdateView.as_view(), name="instructor_edit"),
    path("instructors/<int:pk>/delete/", views.InstructorDeleteView.as_view(), name="instructor_delete"),

    # Enrollments
    path("enrollments/", views.EnrollmentListView.as_view(), name="enrollment_list"),
    path("enrollments/create/", views.EnrollmentCreateView.as_view(), name="enrollment_create"),
    path("enrollments/<int:pk>/", views.EnrollmentDetailView.as_view(), name="enrollment_detail"),
    path("enrollments/<int:pk>/edit/", views.EnrollmentUpdateView.as_view(), name="enrollment_edit"),
    path("enrollments/<int:pk>/delete/", views.EnrollmentDeleteView.as_view(), name="enrollment_delete"),

    # Metadata plain create for quick attach
    path("metadata/", views.MetadataListView.as_view(), name="metadata_list"),
    path("metadata/create/", views.MetadataCreateView.as_view(), name="metadata_create"),
    path("metadata/<int:pk>/update/", views.MetadataUpdateView.as_view(), name="metadata_edit"),
    path("metadata/<int:pk>/delete/", views.MetadataDeleteView.as_view(), name="metadata_delete"),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
