from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_student = models.BooleanField('student status', default=False)
    is_alumni = models.BooleanField('alumni status', default=False)

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    branch = models.CharField(max_length=100)
    year = models.IntegerField(null=True, blank=True)
    interests = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Student"

class AlumniProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='alumni_profile')
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    department = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=100, blank=True)
    experience = models.TextField(blank=True)  # in years or description
    skills = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - Alumni"

class MentorshipRequest(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    )
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests', limit_choices_to={'is_student': True})
    alumni = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests', limit_choices_to={'is_alumni': True})
    message = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} -> {self.alumni.username} ({self.status})"

class Post(models.Model):
    POST_TYPES = (
        ('Job', 'Job'),
        ('Internship', 'Internship'),
        ('Tip', 'Career Tip'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', limit_choices_to={'is_alumni': True})
    title = models.CharField(max_length=200)
    content = models.TextField()
    post_type = models.CharField(max_length=20, choices=POST_TYPES, default='Job')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='events')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username} -> {self.receiver.username}"
