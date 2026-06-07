from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Contribution, Feedback


def contribution_list(request):
    """List all contributions"""
    contributions = Contribution.objects.all().order_by('-date')
    return render(request, 'contributions/contribution_list.html', {'contributions': contributions})


@login_required
def contribution_add(request):
    """Add a new contribution"""
    if request.user.role != 'ALUMNI':
        messages.error(request, 'Only alumni can add contributions.')
        return redirect('contribution_list')
    
    if request.method == 'POST':
        Contribution.objects.create(
            alumnus=request.user,
            contribution_type=request.POST.get('contribution_type'),
            description=request.POST.get('description'),
            amount=request.POST.get('amount') or None,
            date=request.POST.get('date'),
            is_anonymous=request.POST.get('is_anonymous') == 'on'
        )
        messages.success(request, 'Contribution added successfully!')
        return redirect('my_contributions')
    
    return render(request, 'contributions/contribution_add.html')


@login_required
def my_contributions(request):
    """View user's contributions"""
    contributions = Contribution.objects.filter(alumnus=request.user)
    return render(request, 'contributions/my_contributions.html', {'contributions': contributions})


def feedback_list(request):
    """List all feedback"""
    feedbacks = Feedback.objects.all()
    return render(request, 'contributions/feedback_list.html', {'feedbacks': feedbacks})


@login_required
def feedback_add(request):
    """Add feedback"""
    if request.method == 'POST':
        Feedback.objects.create(
            user=request.user,
            category=request.POST.get('category'),
            subject=request.POST.get('subject'),
            message=request.POST.get('message')
        )
        messages.success(request, 'Feedback submitted successfully!')
        return redirect('feedback_list')
    
    return render(request, 'contributions/feedback_add.html')


@login_required
def feedback_respond(request, pk):
    """Respond to feedback (admin only)"""
    if request.user.role != 'ADMIN':
        messages.error(request, 'Only admins can respond to feedback.')
        return redirect('feedback_list')
    
    feedback = get_object_or_404(Feedback, pk=pk)
    
    if request.method == 'POST':
        feedback.admin_response = request.POST.get('response')
        feedback.status = 'RESPONDED'
        feedback.save()
        messages.success(request, 'Response added successfully!')
        return redirect('feedback_list')
    
    return render(request, 'contributions/feedback_respond.html', {'feedback': feedback})
