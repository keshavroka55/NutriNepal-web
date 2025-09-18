from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from tracker.models import Profile
from tracker.forms import ProfileForm
from django.contrib import messages


# Register
def SignUp_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after register
            return redirect('userprofile')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# Profile Page
@login_required
def profile_view(request):
    return render(request, 'profile.html', {'user': request.user})

# Logout
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def profile_edit(request):
    profile = get_object_or_404(Profile, user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('dashboard')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile_form.html', {'form': form})
