from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.http import HttpRequest

User = get_user_model()

@csrf_protect
def signup(request: HttpRequest):
    if request.method == "POST":
        errors = []
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if not len(username) > 3 or User.objects.filter(username=username).exists():
            errors.append('Username is already taken, or is too short.')
        if not len(email) > 0 or User.objects.filter(email=email).exists():
            errors.append('Email must be valid and not belonging to existing user.')
        if not len(password1) > 7 or password1 != password2:
            errors.append('Password is too short, or entered passwords do not match.')
        if len(errors):
            for error in errors:
                messages.error(request, error)
        else:
            User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "Sign up successful. You can login now.")
            return redirect('login')
    return render(request, 'user_profile/signup.html')


