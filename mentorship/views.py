from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AlumniConnectionRequest, JobPosting, JobApplication


def mentorship_list(request):
    """List available alumni"""
    from accounts.models import AlumniProfile
    alumni = AlumniProfile.objects.filter(user__is_active=True)
    return render(request, 'mentorship/mentorship_list.html', {'alumni': alumni})


@login_required
def mentorship_request(request):
    """Request connection from an alumni"""
    if request.user.role != 'STUDENT':
        messages.error(request, 'Only students can request alumni connections.')
        return redirect('alumni_list')
    
    if request.method == 'POST':
        mentor_id = request.POST.get('mentor_id')
        message = request.POST.get('message')
        from accounts.models import User
        mentor = get_object_or_404(User, id=mentor_id, role='ALUMNI')
        
        AlumniConnectionRequest.objects.create(
            alumni=mentor,
            student=request.user,
            subject=message[:200],
            description=message
        )
        messages.success(request, 'Alumni connection request sent successfully!')
        return redirect('alumni_list')
    
    return redirect('alumni_list')


@login_required
def mentorship_requests(request):
    """View alumni connection requests"""
    if request.user.role == 'ALUMNI':
        requests = AlumniConnectionRequest.objects.filter(alumni=request.user)
    elif request.user.role == 'STUDENT':
        requests = AlumniConnectionRequest.objects.filter(student=request.user)
    else:
        requests = AlumniConnectionRequest.objects.all()
    
    return render(request, 'mentorship/mentorship_requests.html', {'requests': requests})


@login_required
def accept_request(request, pk):
    """Accept alumni connection request"""
    alumni_request = get_object_or_404(AlumniConnectionRequest, pk=pk, alumni=request.user)
    alumni_request.status = 'ACCEPTED'
    alumni_request.save()
    messages.success(request, 'Alumni connection request accepted!')
    return redirect('alumni_requests')


@login_required
def reject_request(request, pk):
    """Reject alumni connection request"""
    alumni_request = get_object_or_404(AlumniConnectionRequest, pk=pk, alumni=request.user)
    alumni_request.status = 'REJECTED'
    alumni_request.save()
    messages.success(request, 'Alumni connection request rejected.')
    return redirect('alumni_requests')


def job_list(request):
    """List job postings"""
    jobs = JobPosting.objects.filter(is_active=True).order_by('-created_at')
    return render(request, 'mentorship/job_list.html', {'jobs': jobs})


@login_required
def job_create(request):
    """Create a job posting (alumni only)"""
    if request.user.role != 'ALUMNI':
        messages.error(request, 'Only alumni can post jobs.')
        return redirect('job_list')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        company = request.POST.get('company')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        location = request.POST.get('location')
        job_type = request.POST.get('job_type')
        salary_range = request.POST.get('salary_range') or ''
        application_deadline = request.POST.get('application_deadline')
        
        if not title or not company or not description:
            messages.error(request, 'Title, company, and description are required fields.')
            return render(request, 'mentorship/job_create.html')
        
        JobPosting.objects.create(
            posted_by=request.user,
            title=title,
            company=company,
            description=description,
            requirements=requirements,
            location=location,
            job_type=job_type,
            salary_range=salary_range,
            application_deadline=application_deadline
        )
        messages.success(request, 'Job posted successfully!')
        return redirect('job_list')
    
    return render(request, 'mentorship/job_create.html')


@login_required
def job_apply(request, pk):
    """Apply for a job"""
    job = get_object_or_404(JobPosting, pk=pk)
    
    if JobApplication.objects.filter(job=job, applicant=request.user).exists():
        messages.info(request, 'You have already applied for this job.')
    else:
        JobApplication.objects.create(
            job=job,
            applicant=request.user,
            cover_letter=request.POST.get('cover_letter', '')
        )
        messages.success(request, 'Application submitted successfully!')
    
    return redirect('job_list')


@login_required
def my_jobs(request):
    """View user's job applications"""
    applications = JobApplication.objects.filter(applicant=request.user)
    return render(request, 'mentorship/my_jobs.html', {'applications': applications})
