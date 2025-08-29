from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
# Create your models here.

class Metadata(models.Model):
  key=models.CharField(max_length = 100, db_index = True)
  value=models.TextField(blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    ordering = ['key', 'id']

  def __str__(self):
    return f"{self.key} = {self.value[:30]}"



class Student(models.Model):
  first_name = models.CharField(max_length=80)
  last_name = models.CharField(max_length=80)
  email = models.EmailField(unique=True)
  dob = models.DateField()
  metadata = models.ManyToManyField(Metadata,through='StudentMetadata', blank=True, related_name='students')

  class Meta:
    indexes = [models.Index(fields=['last_name', "first_name"])]

  def clean(self):
    if self.dob > timezone.now().date():
      raise ValidationError("Date Of Birth cannot be in the future.")

  def __str__(self):
    return f"{self.first_name} {self.last_name}"

class StudentMetadata(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    metadata = models.ForeignKey(Metadata, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'metadata')

    def __str__(self):
        return f"{self.student} - {self.metadata.key}"


class Course(models.Model):
  course_name = models.CharField(max_length=200)
  course_code = models.CharField(max_length=20, unique=True)
  description = models.TextField(blank=True)
  metadata  = models.ManyToManyField(Metadata, blank=True, related_name='courses')

  class Meta:
    indexes = [models.Index(fields=['course_code'])]

  def __str__(self):
        return f"{self.course_code} — {self.name}"

class Instructor(models.Model):
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)
    courses = models.ManyToManyField(Course, blank=True, related_name="instructors")
    metadata = models.ManyToManyField(Metadata, blank=True, related_name="instructors")

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Enrollment(models.Model):
  GRADE_CHOICES = [
        ("A", "A"),
        ("B", "B"),
        ("C", "C"),
        ("D", "D"),
        ("F", "F"),
    ]
  student= models.ForeignKey(Student, on_delete= models.CASCADE , related_name= 'enrollments')
  course= models.ForeignKey(Course, on_delete= models.CASCADE , related_name= 'enrollments')
  grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
  metadata = models.ManyToManyField(Metadata, through='EnrollmentMetadata', blank=True, related_name="enrollments")

  class Meta:
        constraints = [
            models.UniqueConstraint(fields=["student", "course"], name="unique_student_course")
        ]

  def __str__(self):
        return f"{self.student} in {self.course}"

class EnrollmentMetadata(models.Model):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE)
    metadata = models.ForeignKey(Metadata, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('enrollment', 'metadata')

    def __str__(self):
        return f"{self.enrollment} - {self.metadata.key}"


