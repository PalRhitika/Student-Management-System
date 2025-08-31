from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Student, Course, Enrollment, Instructor, Metadata

User = get_user_model()


class StudentModelTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            first_name="Rita",
            last_name="Adhikari",
            email="rita@mailinator.com",
            dob="2000-01-01"
        )

    def test_str_method(self):
        self.assertEqual(str(self.student), "Rita Adhikari")

    def test_unique_email(self):
        with self.assertRaises(Exception):
            Student.objects.create(
                first_name="Rita",
                last_name="Adhikari",
                email="rita@mailinator.com",
                dob="2001-01-01"
            )


class StudentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass")
        self.student = Student.objects.create(first_name="Rita", last_name="Adhikari", email="Rita@example.com", dob="2000-01-01")

    def test_student_list_view_as_guest(self):
      response = self.client.get(reverse("student_list"))
      self.assertEqual(response.status_code, 200)
      self.assertContains(response, "Rita")
      self.assertContains(response, "Adhikari")

    def test_student_detail_view_as_guest(self):
        response = self.client.get(reverse("student_detail", args=[self.student.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Rita")
        self.assertContains(response, "Adhikari")

    def test_student_create_view_requires_login(self):
        response = self.client.get(reverse("student_create"))
        self.assertNotEqual(response.status_code, 200)

    def test_student_create_as_superuser(self):
        self.client.login(username="admin", password="adminpass")
        response = self.client.post(reverse("student_create"), {
            "first_name": "Sangita",
            "last_name": "Adhikari",
            "email": "Sangita@example.com",
            "dob": "2001-05-05"
        })
        self.assertEqual(Student.objects.count(), 2)


class CourseModelTest(TestCase):
    def setUp(self):
        self.course = Course.objects.create(
            course_name="Mathematics",
            course_code="MATH101",
            description="Basic Math"
        )

    def test_str_method(self):
        self.assertEqual(str(self.course), "MATH101 — Mathematics")


class InstructorTest(TestCase):
    def setUp(self):
        self.instructor = Instructor.objects.create(
            first_name="Raj",
            last_name="Sharma",
            email="rajsharma@example.com"
        )

    def test_str_method(self):
        self.assertEqual(str(self.instructor), "Raj Sharma")

    def test_instructor_can_teach_multiple_courses(self):
        course1 = Course.objects.create(course_name="Physics", course_code="PHY101", description="Physics Basics")
        course2 = Course.objects.create(course_name="Chemistry", course_code="CHEM101", description="Chemistry Basics")
        self.instructor.courses.add(course1, course2)
        self.assertEqual(self.instructor.courses.count(), 2)
        self.assertIn(course1, self.instructor.courses.all())
        self.assertIn(course2, self.instructor.courses.all())

    def test_instructor_list_view_as_guest(self):
        response = self.client.get(reverse("instructor_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Raj")
        self.assertContains(response, "Sharma")

    def test_instructor_detail_view_as_guest(self):
        response = self.client.get(reverse("instructor_detail", args=[self.instructor.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Raj")
        self.assertContains(response, "Sharma")



class MetadataModelTest(TestCase):
    def setUp(self):
        self.metadata = Metadata.objects.create(
            key="Hobby",
            value="Reading Books"
        )

    def test_str_method(self):
        self.assertIn("Hobby", str(self.metadata))
        self.assertIn("Reading", str(self.metadata))


class EnrollmentTest(TestCase):
    def setUp(self):
        self.student = Student.objects.create(
            first_name="Rita", last_name="Adhikari", email="Rita@example.com", dob="2000-01-01"
        )
        self.course = Course.objects.create(
            course_name="Science", course_code="SCI101", description="Basic Science"
        )

    def test_enrollment_creation(self):
        enrollment = Enrollment.objects.create(student=self.student, course=self.course, grade="A")
        self.assertEqual(str(enrollment), "Rita Adhikari in SCI101 — Science")

    def test_prevent_duplicate_enrollment(self):
        Enrollment.objects.create(student=self.student, course=self.course, grade="B")
        with self.assertRaises(Exception):
            Enrollment.objects.create(student=self.student, course=self.course, grade="A")

    def test_metadata_attaches_correctly(self):
        meta = Metadata.objects.create(key="Attendance", value="95%")
        enrollment = Enrollment.objects.create(student=self.student, course=self.course, grade="A")
        enrollment.metadata.add(meta)
        self.assertIn(meta, enrollment.metadata.all())

    def test_delete_student_deletes_enrollments(self):
        enrollment = Enrollment.objects.create(student=self.student, course=self.course, grade="A")
        self.student.delete()
        self.assertFalse(Enrollment.objects.filter(id=enrollment.id).exists())

    def test_delete_course_deletes_enrollments(self):
        enrollment = Enrollment.objects.create(student=self.student, course=self.course, grade="A")
        self.course.delete()
        self.assertFalse(Enrollment.objects.filter(id=enrollment.id).exists())
