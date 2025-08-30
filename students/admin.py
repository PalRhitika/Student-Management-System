from django.contrib import admin
from .models import Student, Course, Instructor, Enrollment, Metadata, StudentMetadata
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")
    search_fields = ("first_name", "last_name", "email")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_code", "course_name")
    search_fields = ("course_code", "course_name")

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")
    search_fields = ("first_name", "last_name", "email")

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "grade")
    search_fields = ("student__first_name", "student__last_name", "course__course_code")

admin.site.register(Metadata)
admin.site.register(StudentMetadata)
