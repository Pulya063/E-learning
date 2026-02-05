from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import update_session_auth_hash

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
            return redirect("main_page")
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


def user_page(request, user_id):
    target_user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        if not request.user.is_authenticated or request.user.id != target_user.id:
            messages.error(request, "You do not have permission to edit this profile.")
            return redirect('login')

        target_user.username = request.POST.get('username')
        target_user.first_name = request.POST.get('first_name')
        target_user.last_name = request.POST.get('last_name')
        target_user.email = request.POST.get('email')

        password = request.POST.get('password')
        if password:
            target_user.set_password(password)
            target_user.save()
            update_session_auth_hash(request, target_user)
        else:
            target_user.save()

        messages.success(request, "Profile updated successfully!")
        return redirect('main_page')

    return render(request, 'user_page.html', {'target_user': target_user})

def main_page(request):
    if request.user.groups.filter(name='Teachers').exists():
        return redirect('teacher_page')
    elif request.user.groups.filter(name='Students').exists():
        return redirect('student_page')
    elif request.user.groups.filter(name='Parents').exists():
        return redirect('parent_page')
    else:
        messages.error(request, "Please login first.")
        return redirect('login')