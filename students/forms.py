from django import forms
from .models import Student, Course, Instructor, Enrollment, Metadata
from django.core.exceptions import ValidationError
from django.utils import timezone
# Student Form
class StudentForm(forms.ModelForm):
    metadata = forms.ModelMultipleChoiceField(
        queryset=Metadata.objects.all(),
        required=False,
         widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Student
        fields = ["first_name", "last_name", "email", "dob", "metadata"]
        widgets = {"dob": forms.DateInput(attrs={"type": "date", "class": "form-control"})}

    def clean_dob(self):
        dob = self.cleaned_data.get("dob")
        if dob and dob > timezone.now().date():
            raise ValidationError("Date of Birth cannot be in the future.")
        return dob

# Course Form
class CourseForm(forms.ModelForm):
    metadata = forms.ModelMultipleChoiceField(
        queryset=Metadata.objects.all(),
        required=False,
         widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Course
        fields = ["course_name", "course_code", "description", "metadata"]
        widgets = {
            "course_name": forms.TextInput(attrs={"class": "form-control"}),
            "course_code": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }


# Instructor Form
class InstructorForm(forms.ModelForm):
    metadata = forms.ModelMultipleChoiceField(
        queryset=Metadata.objects.all(),
        required=False,
         widget=forms.CheckboxSelectMultiple
    )
    courses = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        required=False,
         widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Instructor
        fields = ["first_name", "last_name", "email", "courses", "metadata"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "courses": forms.SelectMultiple(attrs={"class": "form-select"}),
        }


# Enrollment Form
class EnrollmentForm(forms.ModelForm):
    metadata = forms.ModelMultipleChoiceField(
        queryset=Metadata.objects.all(),
        required=False,
         widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = Enrollment
        fields = ["student", "course", "exam_score", "grade", "metadata"]
        widgets = {
            "student": forms.Select(attrs={"class": "form-select form-select-lg mb-3"}),
            "course": forms.Select(attrs={"class": "form-select form-select-lg mb-3"}),
            "exam_score": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "Enter exam score"}),
            "grade": forms.Select(attrs={"class": "form-select"}),
        }


# Metadata Form
class MetadataForm(forms.ModelForm):
    class Meta:
        model = Metadata
        fields = ["key", "value"]
        widgets = {
            "key": forms.TextInput(attrs={"class": "form-control"}),
            "value": forms.TextInput(attrs={"class": "form-control"}),
        }
