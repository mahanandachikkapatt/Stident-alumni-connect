from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom User model with role-based access"""
    
    ROLE_CHOICES = [
        ('ALUMNI', 'Alumni'),
        ('STUDENT', 'Student'),
        ('ADMIN', 'Administrator'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='STUDENT')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.png', blank=True)
    bio = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    @property
    def is_alumni(self):
        return self.role == 'ALUMNI'
    
    @property
    def is_student(self):
        return self.role == 'STUDENT'
    
    @property
    def is_admin_user(self):
        return self.role == 'ADMIN' or self.is_superuser


class AlumniProfile(models.Model):
    """Alumni specific profile information"""
    
    BATCH_CHOICES = [(str(year), str(year)) for year in range(2000, 2030)]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alumni_profile')
    graduation_year = models.CharField(max_length=4, choices=BATCH_CHOICES)
    degree = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    current_company = models.CharField(max_length=200, blank=True)
    current_position = models.CharField(max_length=100, blank=True)
    work_experience = models.TextField(blank=True)
    skills = models.TextField(blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True)
    is_available_for_mentoring = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Alumni Profile: {self.user.get_full_name() or self.user.username}"


class StudentProfile(models.Model):
    """Student specific profile information"""
    
    BATCH_CHOICES = [(str(year), str(year)) for year in range(2020, 2030)]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    enrollment_year = models.CharField(max_length=4, choices=BATCH_CHOICES)
    department = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, blank=True)
    semester = models.IntegerField(default=1)
    skills_interest = models.TextField(blank=True)
    career_goals = models.TextField(blank=True)
    is_looking_for_internship = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Student Profile: {self.user.get_full_name() or self.user.username}"
