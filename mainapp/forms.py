from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, AlumniProfile, Post

class CustomUserCreationForm(UserCreationForm):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('alumni', 'Alumni'),
    )
    role = forms.ChoiceField(choices=ROLE_CHOICES, widget=forms.RadioSelect, initial='student')
    
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', )

    def save(self, commit=True):
        user = super().save(commit=False)
        role = self.cleaned_data.get('role')
        if role == 'student':
            user.is_student = True
        elif role == 'alumni':
            user.is_alumni = True
        if commit:
            user.save()
            if user.is_student:
                StudentProfile.objects.create(user=user)
            elif user.is_alumni:
                AlumniProfile.objects.create(user=user)
        return user

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['profile_picture', 'resume', 'branch', 'year', 'interests']

class AlumniProfileForm(forms.ModelForm):
    class Meta:
        model = AlumniProfile
        fields = ['profile_picture', 'department', 'company', 'role', 'experience', 'skills']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'post_type']
