from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100)
    course_code = models.CharField(max_length=20, unique=True)
    faculty = models.ForeignKey("users.Faculty", on_delete=models.CASCADE)  # String reference
    students = models.ManyToManyField("users.Student", related_name='courses')  # String reference

    def __str__(self):
        return self.name
