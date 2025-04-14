from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import logging

# 🔹 Setup Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('app.log')
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 🔹 Custom User Model
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('faculty', 'Faculty'),
        ('student', 'Student'),
        ('staff', 'Staff'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')

    def save(self, *args, **kwargs):
        logger.info(f"User {self.username} saved")
        super().save(*args, **kwargs)

# 🔹 Student Model
class Student(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='male')
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    photo = models.ImageField(upload_to='student_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        logger.info(f"Student {self.user.username} saved")
        super().save(*args, **kwargs)

# 🔹 Faculty Model
class Faculty(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    faculty_id = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=True)
    photo = models.ImageField(upload_to='faculty_photos/', null=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        logger.info(f"Faculty {self.user.username} saved")
        super().save(*args, **kwargs)

# 🔹 Course Model
class Course(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=50, unique=True)
    total_assignments = models.PositiveIntegerField(default=10)
    total_classes = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.name

# 🔹 Enrollment Model
class Enrollment(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_assignments = models.PositiveIntegerField(default=0)
    attended_classes = models.PositiveIntegerField(default=0)
    progress = models.FloatField(default=0.0)

    def calculate_progress(self):
        assignment_weight = 0.5
        attendance_weight = 0.5

        assignment_progress = (
            (self.completed_assignments / self.course.total_assignments) * 100
            if self.course.total_assignments else 0
        )
        attendance_progress = (
            (self.attended_classes / self.course.total_classes) * 100
            if self.course.total_classes else 0
        )

        overall_progress = (assignment_progress * assignment_weight) + (attendance_progress * attendance_weight)
        return round(overall_progress, 2)

    def save(self, *args, **kwargs):
        self.progress = self.calculate_progress()
        logger.info(f"Enrollment: {self.student.username} - {self.course.name} saved with progress {self.progress}%")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.username} - {self.course.name} ({self.progress}% progress)"
