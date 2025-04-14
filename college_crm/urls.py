from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from users.views import home_view  # Import your actual dashboard view

# Define a simple home view (remove this if you're using home_view instead)
def home(request):
    return HttpResponse("<h1>Welcome to College CRM</h1>")

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # Choose ONE of these root URL patterns:
    # Option 1: Use your dashboard view (recommended)
    path("", home_view, name="home"),
    
    # Option 2: Use the simple welcome message
    # path("", home, name="home"),
    
    # Other URL patterns
    path("users/", include("users.urls")),
    path('dashboard/', home_view, name='dashboard'),
]