from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get("username"),
            password=request.POST.get("password")
        )

        if user:
            login(request, user)
            messages.success(request, "Welcome!")
            return redirect("user_page", user_id=user.id)
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
    else:
        return render(request, "login.html")

def register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        new_user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        new_user.save()
        messages.success(request, "You are registered")
        return redirect("login")
    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User

def user_page(request, user_id):
    # Use get_object_or_404 to prevent a 500 error if the ID is wrong
    target_user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        # Security Check
        if not request.user.is_authenticated or request.user.id != target_user.id:
            messages.error(request, "You do not have permission to edit this profile.")
            return redirect('login')

        # Update basic info
        target_user.username = request.POST.get('username')
        target_user.first_name = request.POST.get('first_name')
        target_user.last_name = request.POST.get('last_name')
        target_user.email = request.POST.get('email')

        # Handle password specifically
        password = request.POST.get('password')
        if password:
            target_user.set_password(password)
            target_user.save()
            # CRITICAL: Keep the session active after password change
            update_session_auth_hash(request, target_user)
        else:
            target_user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('user_page', user_id=target_user.id)

    return render(request, 'user_page.html', {'target_user': target_user})

def lesson(request, lesson_id):
    return ""