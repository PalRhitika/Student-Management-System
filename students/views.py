from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Student, Course, Instructor, Enrollment, Metadata
from .forms import StudentForm, CourseForm, InstructorForm, EnrollmentForm, MetadataForm, StudentMetadataFormSet
from django.shortcuts import redirect, render
class MetadataCreateView(LoginRequiredMixin, CreateView):
    model = Metadata
    form_class = MetadataForm
    template_name = "metadata/metadata_form.html"
    success_url = reverse_lazy("home")

class SearchPaginateListView(ListView):
    paginate_by = 10
    search_fields = []

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get("q")
        if q and self.search_fields:
            cond = Q()
            for f in self.search_fields:
                cond |= Q(**{f"{f}__icontains": q})
            qs = qs.filter(cond)
        key = self.request.GET.get("meta_key")
        val = self.request.GET.get("meta_val")
        if key:
            qs = qs.filter(metadata__key__icontains=key)
        if val:
            qs = qs.filter(metadata__value__icontains=val)
        return qs.distinct()

# Student
class StudentListView(SearchPaginateListView):
    model = Student
    search_fields = ["first_name", "last_name", "email", "metadata"]
    template_name = "students/student_list.html"
    context_object_name = "students"

    def get_queryset(self):
        # Optional: add ordering
        return Student.objects.prefetch_related('studentmetadata_set__metadata').order_by('last_name', 'first_name')

class StudentDetailView(DetailView):
    model = Student
    template_name = "students/student_detail.html"




class StudentCreateView(LoginRequiredMixin, CreateView):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("student_list")

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = StudentMetadataFormSet()
        return render(request, self.template_name, {"form": form, "formset": formset})

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        formset = StudentMetadataFormSet(self.request.POST)

        if form.is_valid() and formset.is_valid():
            student = form.save()
            formset.instance = student
            formset.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {"form": form, "formset": formset})



class StudentUpdateView(LoginRequiredMixin, UpdateView):
    model = Student
    form_class = StudentForm
    template_name = "students/student_form.html"
    success_url = reverse_lazy("student_list")
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = StudentMetadataFormSet(instance=self.object)
        return render(request, self.template_name, {"form": form, "formset": formset})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        formset = StudentMetadataFormSet(self.request.POST, instance=self.object)

        if form.is_valid() and formset.is_valid():
            student = form.save()
            formset.instance = student
            formset.save()
            return redirect(self.success_url)

        return render(request, self.template_name, {"form": form, "formset": formset})

class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = Student
    template_name = "students/student_delete.html"
    success_url = reverse_lazy("student_list")

# Course
class CourseListView(SearchPaginateListView):
    model = Course
    search_fields = ["name", "course_code"]
    template_name = "courses/course_list.html"

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
    template_name = "courses/confirm_delete.html"
    success_url = reverse_lazy("course_list")

# Instructor
class InstructorListView(SearchPaginateListView):
    model = Instructor
    search_fields = ["first_name", "last_name", "email"]
    template_name = "instructors/instructor_list.html"

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
    search_fields = ["student__first_name", "student__last_name", "course__course_code"]
    template_name = "enrollments/enrollment_list.html"

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


