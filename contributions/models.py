from django.db import models
from django.conf import settings


class Contribution(models.Model):
    """Alumni contributions tracking"""
    
    CONTRIBUTION_TYPES = [
        ('FINANCIAL', 'Financial'),
        ('MENTORING', 'Mentoring'),
        ('EVENT_SUPPORT', 'Event Support'),
        ('GUEST_LECTURE', 'Guest Lecture'),
        ('OTHER', 'Other'),
    ]
    
    alumnus = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='contributions')
    contribution_type = models.CharField(max_length=20, choices=CONTRIBUTION_TYPES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateField()
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.alumnus.username} - {self.get_contribution_type_display()}"


class Feedback(models.Model):
    """Feedback from alumni and students"""
    
    CATEGORY_CHOICES = [
        ('GENERAL', 'General'),
        ('WEBSITE', 'Website'),
        ('EVENTS', 'Events'),
        ('MENTORSHIP', 'Mentorship'),
        ('SUGGESTION', 'Suggestion'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('REVIEWED', 'Reviewed'),
        ('RESPONDED', 'Responded'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='feedbacks')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='GENERAL')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    admin_response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Feedback: {self.subject}"
