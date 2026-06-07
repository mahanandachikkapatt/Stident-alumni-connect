from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
from .models import AlumniProfile, StudentProfile
from .forms import AlumniRegistrationForm, StudentRegistrationForm, UserUpdateForm, ProfileUpdateForm


def home(request):
    """Home page view"""
    from events.models import Event
    from messaging.models import Announcement
    
    upcoming_events = Event.objects.filter(date__gte=datetime.now()).order_by('date')[:6]
    announcements = Announcement.objects.all().order_by('-created_at')[:3]
    
    context = {
        'events': upcoming_events,
        'announcements': announcements,
    }
    return render(request, 'accounts/home.html', context)


def alumni_register(request):
    """Alumni registration view"""
    if request.method == 'POST':
        form = AlumniRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create alumni profile
            AlumniProfile.objects.create(
                user=user,
                graduation_year=form.cleaned_data.get('graduation_year'),
                department=form.cleaned_data.get('department'),
                degree=form.cleaned_data.get('degree'),
            )
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Alumni Connect.')
            return redirect('dashboard')
    else:
        form = AlumniRegistrationForm()
    return render(request, 'accounts/alumni_register.html', {'form': form})


def student_register(request):
    """Student registration view"""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create student profile
            StudentProfile.objects.create(
                user=user,
                enrollment_year=form.cleaned_data.get('enrollment_year'),
                department=form.cleaned_data.get('department'),
            )
            login(request, user)
            messages.success(request, 'Registration successful! Welcome to Alumni Connect.')
            return redirect('dashboard')
    else:
        form = StudentRegistrationForm()
    return render(request, 'accounts/student_register.html', {'form': form})


@login_required
def dashboard(request):
    """User dashboard view"""
    context = {
        'user': request.user,
    }
    return render(request, 'accounts/dashboard.html', context)


@login_required
def profile(request):
    """User profile view"""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def profile_edit(request):
    """Profile edit view"""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if 'profile_picture' in request.FILES:
            request.user.profile_picture = request.FILES['profile_picture']
            request.user.save()
        
        if u_form.is_valid():
            u_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
        else:
            # Add form errors to messages for debugging
            for field, errors in u_form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        u_form = UserUpdateForm(instance=request.user)
    
    context = {
        'u_form': u_form,
    }
    return render(request, 'accounts/profile_edit.html', context)
