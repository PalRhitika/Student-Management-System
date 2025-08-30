from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Student, Course, Instructor, Enrollment, Metadata
from .forms import StudentForm, CourseForm, InstructorForm, EnrollmentForm, MetadataForm

# Parent list view class
class SearchPaginateListView(ListView):
    paginate_by = 10
    search_fields = []

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q", "").strip()

        if q and self.search_fields:
            cond = Q()
            for f in self.search_fields:
                if not f:
                    continue
                if "__" in f:
                    cond |= Q(**{f: q})
                else:
                    cond |= Q(**{f"{f}__icontains": q})
            qs = qs.filter(cond)

        key = self.request.GET.get("meta_key", "").strip()
        val = self.request.GET.get("meta_val", "").strip()
        if key:
            qs = qs.filter(metadata__key__icontains=key)
        if val:
            qs = qs.filter(metadata__value__icontains=val)

        return qs.distinct()



#Metadata CRUD
class MetadataListView(LoginRequiredMixin, SearchPaginateListView):
    model = Metadata
    template_name = "metadata/metadata_list.html"
    context_object_name = "metadata"
    search_fields=['key','value']
    def get_queryset(self):
        qs = super().get_queryset().order_by("key", "value")
        return qs

class MetadataCreateView(LoginRequiredMixin, CreateView):
    model = Metadata
    form_class = MetadataForm
    template_name = "metadata/metadata_form.html"
    success_url = reverse_lazy("metadata_list")

class MetadataUpdateView(LoginRequiredMixin, UpdateView):
    model = Metadata
    form_class = MetadataForm
    template_name = "metadata/metadata_form.html"
    success_url = reverse_lazy("metadata_list")

class MetadataDeleteView(LoginRequiredMixin, DeleteView):
    model = Metadata
    template_name = "metadata/metadata_delete.html"
    success_url = reverse_lazy("metadata_list")




#Student CRUD:
class StudentListView(SearchPaginateListView):
    model = Student
    template_name = "students/student_list.html"
    context_object_name = "students"
    search_fields = ["first_name", "last_name", "email"]
    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("metadata").order_by("last_name", "first_name")
        return qs



class StudentDetailView(DetailView):
    model = Student
    template_name = "students/student_detail.html"

class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("student_list")


class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("student_list")

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = "students/student_delete.html"
    success_url = reverse_lazy("student_list")

# Course CRUD
class CourseListView(SearchPaginateListView):
    model = Course
    context_object_name = "courses"
    search_fields=['course_name', 'course_code']
    template_name = "courses/course_list.html"
    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("metadata").order_by("course_name", "course_code")
        return qs


class CourseDetailView(DetailView):
    model = Course
    template_name = "courses/course_detail.html"

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy("course_list")

class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = "courses/course_form.html"
    success_url = reverse_lazy("course_list")

class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = "courses/course_delete.html"
    success_url = reverse_lazy("course_list")

# Instructor
class InstructorListView(SearchPaginateListView):
    model = Instructor
    search_fields = ["first_name", "last_name", "email", "courses__course_name", "courses__course_code"]
    template_name = "instructors/instructor_list.html"
    context_object_name="instructors"
    def get_queryset(self):
        qs = super().get_queryset().prefetch_related("metadata","courses").order_by("first_name", "last_name")
        return qs


class InstructorDetailView(DetailView):
    model = Instructor
    template_name = "instructors/instructor_detail.html"

class InstructorCreateView(LoginRequiredMixin, CreateView):
    model = Instructor
    form_class = InstructorForm
    template_name = "instructors/instructor_form.html"
    success_url = reverse_lazy("instructor_list")

class InstructorUpdateView(LoginRequiredMixin, UpdateView):
    model = Instructor
    form_class = InstructorForm
    template_name = "instructors/instructor_form.html"
    success_url = reverse_lazy("instructor_list")

class InstructorDeleteView(LoginRequiredMixin, DeleteView):
    model = Instructor
    template_name = "instructors/confirm_delete.html"
    success_url = reverse_lazy("instructor_list")

# Enrollment
class EnrollmentListView(SearchPaginateListView):
    model = Enrollment
    search_fields = ["student__first_name", "student__last_name", "course__course_code", "exam_score", "grade"]
    template_name = "enrollments/enrollment_list.html"
    context_object_name="enrollments"
    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("student", "course").prefetch_related("metadata")
        qs = qs.order_by("student__last_name", "student__first_name", "course__course_code")
        return qs

class EnrollmentDetailView(DetailView):
    model = Enrollment
    template_name = "enrollments/enrollment_detail.html"

class EnrollmentCreateView(LoginRequiredMixin, CreateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = "enrollments/enrollment_form.html"
    success_url = reverse_lazy("enrollment_list")

class EnrollmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Enrollment
    form_class = EnrollmentForm
    template_name = "enrollments/enrollment_form.html"
    success_url = reverse_lazy("enrollment_list")

class EnrollmentDeleteView(LoginRequiredMixin, DeleteView):
    model = Enrollment
    template_name = "enrollments/confirm_delete.html"
    success_url = reverse_lazy("enrollment_list")


