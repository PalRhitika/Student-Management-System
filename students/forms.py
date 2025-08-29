from django import forms
from .models import Student, Course, Instructor, Enrollment, Metadata, StudentMetadata
from django.forms import inlineformset_factory
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["first_name", "last_name", "email", "dob"]
        widgets = {"dob": forms.DateInput(attrs={"type": "date"})}

class StudentMetadataForm(forms.ModelForm):
    class Meta:
        model = StudentMetadata
        fields = ['metadata', 'notes']
        widgets = {
            'metadata': forms.Select(attrs={"class": "form-select"}),
            'notes': forms.TextInput(attrs={"placeholder": "Optional notes"})
        }

StudentMetadataFormSet = inlineformset_factory(
    Student, StudentMetadata, form=StudentMetadataForm,
    extra=1, can_delete=True
)
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["course_name", "course_code", "description", "metadata"]

class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ["first_name", "last_name", "email", "courses", "metadata"]

class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ["student", "course", "grade", "metadata"]

class MetadataForm(forms.ModelForm):

    class Meta:
        model = Metadata
        fields = ["key", "value"]


