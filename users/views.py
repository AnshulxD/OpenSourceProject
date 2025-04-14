from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Course, Enrollment, Student, Faculty
from django.contrib.auth.forms import UserChangeForm
import datetime
import random

User = get_user_model()

# ------------------------- LANDING PAGE -------------------------
def landing_page(request):
    return render(request, "users/landing.html")

# ------------------------- DASHBOARDS -------------------------
@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect("faculty_dashboard")
    return redirect("student_dashboard")

@login_required
def student_dashboard(request):
    try:
        student = request.user.student
        enrollments = Enrollment.objects.filter(student=student).select_related('course')
        enrolled_course_ids = enrollments.values_list('course_id', flat=True)
        available_courses = Course.objects.exclude(id__in=enrolled_course_ids)
    except Student.DoesNotExist:
        messages.error(request, "Student profile not found")
        return redirect('profile')
    
    return render(request, 'users/student_dashboard.html', {
        'enrollments': enrollments,
        'available_courses': available_courses,
    })

@login_required
def faculty_dashboard(request):
    if not request.user.is_staff:
        return redirect('student_dashboard')
    return render(request, "users/faculty_dashboard.html")

# ------------------------- COURSE MANAGEMENT -------------------------
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, "users/course_list.html", {"courses": courses})

@login_required
def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    try:
        student = request.user.student
    except Student.DoesNotExist:
        messages.error(request, "Only students can enroll in courses")
        return redirect('student_dashboard')

    if Enrollment.objects.filter(student=student, course=course).exists():
        messages.warning(request, "You are already enrolled in this course")
    else:
        Enrollment.objects.create(student=student, course=course)
        messages.success(request, f"Successfully enrolled in {course.name}")
    
    return redirect("course_list")

@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    return render(request, "users/my_courses.html", {"enrollments": enrollments})

@login_required
def unenroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == "POST":
        enrollment = Enrollment.objects.filter(student=request.user, course=course).first()
        if enrollment:
            enrollment.delete()
            messages.success(request, f'Unenrolled from {course.name}')
        else:
            messages.error(request, 'Not enrolled in this course')
        return redirect('my_courses')

    return render(request, "users/confirm_unenroll.html", {"course": course})

# ------------------------- ATTENDANCE -------------------------
@login_required
def attendance(request):
    mca_subjects = [
        "Data Structures & Algorithms",
        "Operating Systems",
        "Database Management Systems",
        "Computer Networks",
        "Software Engineering",
        "Web Technologies",
        "Artificial Intelligence",
        "Machine Learning",
        "Cyber Security",
        "Cloud Computing"
    ]

    attendance_data = [
        {"course": subject, "date": datetime.date.today(), "status": "Present" if i % 2 == 0 else "Absent"}
        for i, subject in enumerate(mca_subjects)
    ]
    
    return render(request, "users/attendance.html", {"attendance_data": attendance_data})

# ------------------------- USER AUTHENTICATION -------------------------
def register_user(request):
    if request.method == "POST":
        form_data = request.POST
        if form_data["password"] != form_data["confirm_password"]:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=form_data["username"]).exists():
            messages.error(request, "Username already taken")
            return redirect("register")

        if User.objects.filter(email=form_data["email"]).exists():
            messages.error(request, "Email already registered")
            return redirect("register")

        is_faculty = form_data.get("is_faculty") == "on"
        user = User.objects.create_user(
            username=form_data["username"],
            password=form_data["password"],
            email=form_data["email"],
            first_name=form_data["first_name"],
            last_name=form_data["last_name"],
            is_staff=is_faculty
        )

        if is_faculty:
            Faculty.objects.create(user=user)
        else:
            Student.objects.create(user=user)

        messages.success(request, "Registration successful! Please login.")
        return redirect("login")

    return render(request, "users/register.html")

def login_user(request):
    if request.method == "POST":
        user = authenticate(
            username=request.POST["username"],
            password=request.POST["password"]
        )
        
        if user:
            login(request, user)
            messages.success(request, "Login successful!")
            return redirect("faculty_dashboard" if user.is_staff else "student_dashboard")
        
        messages.error(request, "Invalid credentials")
    
    return render(request, "users/login.html")

def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect("login")

# ------------------------- PROFILE MANAGEMENT -------------------------
@login_required
def profile(request):
    enrollments = Enrollment.objects.filter(student=request.user).select_related('course')
    return render(request, "users/profile.html", {"enrollments": enrollments})

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated!")
            return redirect("profile")
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, "users/edit_profile.html", {"form": form})

# ------------------------- ADMINISTRATION -------------------------
@login_required
def manage_enrollments(request):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    enrollments = Enrollment.objects.filter(
        course__instructor=request.user
    ).select_related('student', 'course')
    
    return render(request, 'faculty/manage_enrollments.html', {
        'enrollments': enrollments
    })

@login_required
def student_list(request):
    if not request.user.is_staff:
        return redirect('student_dashboard')
    return render(request, 'users/student_list.html', {
        'students': Student.objects.all()
    })

@login_required
def course_summary(request):
    enrollments = Enrollment.objects.filter(
        student=request.user
    ).select_related('course')
    return render(request, 'users/course_summary.html', {
        'enrollments': enrollments
    })

@login_required
def manage_courses(request):
    if not request.user.is_staff:
        return redirect('student_dashboard')
    return render(request, 'users/manage_courses.html', {
        'courses': Course.objects.filter(instructor=request.user)
    })

@login_required
def review_performance(request):
    if not request.user.is_staff:
        return redirect('student_dashboard')
        
    enrollments = Enrollment.objects.filter(
        course__instructor=request.user
    ).select_related('student', 'course')
    
    return render(request, 'users/review_performance.html', {
        'enrollments': enrollments
    })

# ------------------------- HOME PAGE -------------------------
@login_required
def home_view(request):
    return render(request, 'users/home.html', {
        'user': request.user
    })