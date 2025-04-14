from django.contrib import admin
from .models import Course, Enrollment, Faculty, CustomUser, Student

# Register CustomUser so it works with autocomplete_fields
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ['username', 'email']  # Enable search by username/email
    list_display = ['username', 'email', 'first_name', 'last_name']

# Register Student so it can be used in EnrollmentAdmin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    search_fields = ['user__username']  # ✅ Removed 'student_id'
    list_display = ['user', 'gender', 'date_of_birth', 'phone_number', 'address']  # ✅ No student_id

# Register Course
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')  
    search_fields = ('name', 'code')

# Register Enrollment
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'progress')  
    search_fields = ('student__user__username', 'course__name')  # ✅ Fix field lookup
    autocomplete_fields = ['student', 'course']  # Student is now registered!

# Register Faculty
admin.site.register(Faculty)
