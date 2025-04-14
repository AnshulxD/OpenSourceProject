from django.urls import path
from .views import (
    dashboard,
    landing_page,
    course_list,
    enroll_course,
    my_courses,
    unenroll_course,
    register_user,
    login_user,
    logout_user,
    profile,
    edit_profile,
    student_dashboard,
    faculty_dashboard,
    attendance,
    manage_enrollments,
    manage_courses,
    home_view,
    student_list,
    course_summary,
    review_performance
)

urlpatterns = [
    # General Pages
    path('', home_view, name='home'),
    path('welcome/', landing_page, name='landing_page'),
    path('dashboard/', dashboard, name='dashboard'),
    
    # Student Routes
    path("courses/", course_list, name="course_list"),  # Changed from "student/courses/"
    path("enroll/<int:course_id>/", enroll_course, name="enroll_course"),
    path("student_dashboard/", student_dashboard, name='student_dashboard'),
    path("my-courses/", my_courses, name='my_courses'),
    path("unenroll/<int:course_id>/", unenroll_course, name="unenroll_course"),
    path("attendance/", attendance, name="attendance"),
    path("student_list/", student_list, name='student_list'),
    path("course-summary/", course_summary, name='course_summary'),
    
    # Faculty Routes
    path('faculty/dashboard/', faculty_dashboard, name='faculty_dashboard'),
    path('faculty/manage-enrollments/', manage_enrollments, name='manage_enrollments'),
    path('faculty/manage-courses/', manage_courses, name='manage_courses'),
    path('faculty/track-attendance/', attendance, name='track_attendance'),
    path('faculty/review-performance/', review_performance, name='review_performance'),
    
    # Authentication
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]   