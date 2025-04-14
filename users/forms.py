from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserLoginForm
from .models import CustomUser, Student
from django import forms

# Register View
def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Change 'home' to your dashboard or homepage
    else:
        form = CustomUserCreationForm()
    return render(request, "users/register.html", {"form": form})

# Login View
def login_user(request):
    if request.method == "POST":
        form = CustomUserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  
    else:
        form = CustomUserLoginForm()
    return render(request, "users/login.html", {"form": form})

# Logout View
def logout_user(request):
    logout(request)
    return redirect("login")  


class CustomUserCreationForm(UserCreationForm):
    is_faculty = forms.BooleanField(required=False, label="Register as Faculty")
    gender = forms.ChoiceField(choices=Student.GENDER_CHOICES, required=False)
    date_of_birth = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    phone_number = forms.CharField(required=False)
    address = forms.CharField(widget=forms.Textarea, required=False)
    photo = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

class CustomUserLoginForm(AuthenticationForm):
    pass