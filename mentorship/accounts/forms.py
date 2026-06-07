from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import AlumniProfile, StudentProfile, User


class AlumniRegistrationForm(UserCreationForm):
    """Form for alumni registration"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    graduation_year = forms.ChoiceField(choices=[(str(y), str(y)) for y in range(2000, 2030)], widget=forms.Select(attrs={'class': 'form-select'}))
    department = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    degree = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = 'ALUMNI'
        if commit:
            user.save()
        return user


class StudentRegistrationForm(UserCreationForm):
    """Form for student registration"""
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    enrollment_year = forms.ChoiceField(choices=[(str(y), str(y)) for y in range(2020, 2030)], widget=forms.Select(attrs={'class': 'form-select'}))
    department = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = 'STUDENT'
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """Form for updating user information"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'address', 'date_of_birth', 'bio']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }


class ProfileUpdateForm(forms.ModelForm):
    """Form for updating profile picture"""
    
    class Meta:
        model = User
        fields = ['profile_picture']
