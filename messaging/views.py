from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Conversation, Message, Announcement

User = get_user_model()


@login_required
def inbox(request):
    """User's inbox with conversations"""
    conversations = Conversation.objects.filter(participants=request.user)
    return render(request, 'messaging/inbox.html', {'conversations': conversations})


@login_required
def compose_message(request):
    """Compose a new message"""
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient_id')
        subject = request.POST.get('subject')
        content = request.POST.get('content')
        
        recipient = get_object_or_404(User, id=recipient_id)
        
        # Create conversation
        conversation = Conversation.objects.create(subject=subject)
        conversation.participants.add(request.user, recipient)
        
        # Create message
        Message.objects.create(
            conversation=conversation,
            sender=request.user,
            content=content
        )
        
        messages.success(request, 'Message sent successfully!')
        return redirect('inbox')
    
    # Get all users except current user
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'messaging/compose.html', {'users': users})


@login_required
def conversation_detail(request, pk):
    """View conversation details and messages"""
    conversation = get_object_or_404(Conversation, pk=pk, participants=request.user)
    
    if request.method == 'POST':
        content = request.POST.get('message')
        if content:  # Ensure content is not empty
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
        return redirect('conversation_detail', pk=pk)
    
    # Mark messages as read
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    return render(request, 'messaging/conversation.html', {'conversation': conversation})


def announcements(request):
    """View announcements"""
    announcements_list = Announcement.objects.filter(is_published=True)
    return render(request, 'messaging/announcements.html', {'announcements': announcements_list})


@login_required
def create_announcement(request):
    """Create announcement (admin only)"""
    if request.user.role != 'ADMIN':
        messages.error(request, 'Only admins can create announcements.')
        return redirect('announcements')
    
    if request.method == 'POST':
        Announcement.objects.create(
            title=request.POST.get('title'),
            content=request.POST.get('content'),
            created_by=request.user
        )
        messages.success(request, 'Announcement created successfully!')
        return redirect('announcements')
    
    return render(request, 'messaging/create_announcement.html')
