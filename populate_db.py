import os
import django
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'alumni_connect.settings')
django.setup()

from mainapp.models import User, StudentProfile, AlumniProfile, MentorshipRequest, Post, Event
from django.utils import timezone

def populate():
    print("Clearing old data...")
    User.objects.all().delete()
    Event.objects.all().delete()

    print("Creating admin user...")
    admin = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    # Adding an attribute for the view logic
    admin.is_admin = True
    admin.save()
    
    print("Creating students...")
    student1 = User.objects.create_user(username='student1', password='password123', first_name='John', last_name='Doe', is_student=True)
    StudentProfile.objects.create(user=student1, branch='Computer Science', year=3, interests='Artificial Intelligence, Web Development')

    student2 = User.objects.create_user(username='student2', password='password123', first_name='Jane', last_name='Smith', is_student=True)
    StudentProfile.objects.create(user=student2, branch='Information Technology', year=2, interests='Cybersecurity, Data Science')

    print("Creating alumni...")
    alumni1 = User.objects.create_user(username='alumni1', password='password123', first_name='Alice', last_name='Johnson', is_alumni=True)
    AlumniProfile.objects.create(user=alumni1, department='Computer Science', company='Google', role='Software Engineer', experience='3 Years', skills='Python, Django, React', is_verified=True)

    alumni2 = User.objects.create_user(username='alumni2', password='password123', first_name='Bob', last_name='Williams', is_alumni=True)
    # Keeping alumni2 unverified for admin testing
    AlumniProfile.objects.create(user=alumni2, department='Electronics', company='Tesla', role='Hardware Engineer', experience='5 Years', skills='C++, Embedded Systems, Robotics', is_verified=False)

    print("Creating posts...")
    Post.objects.create(author=alumni1, title='Software Engineering Internship 2026', content='We are looking for passionate 3rd year students to join our summer internship program at Google. Apply soon!', post_type='Internship')
    Post.objects.create(author=alumni1, title='How to crack tech interviews', content='Always focus on Data Structures and System Design for core tech roles. Good luck everyone.', post_type='Tip')
    
    print("Creating events...")
    Event.objects.create(title='Annual Tech Meetup 2026', description='Join us for the biggest tech meetup of the year! Connect with industry leaders and fellow students.', date=timezone.now() + timedelta(days=15), location='Main Auditorium', created_by=admin)
    Event.objects.create(title='Resume Building Workshop', description='Learn how to build a resume that gets past the ATS system.', date=timezone.now() + timedelta(days=5), location='Seminar Hall B', created_by=admin)

    print("Creating mentorship requests...")
    MentorshipRequest.objects.create(student=student1, alumni=alumni1, message='Hi Alice, I would love to be mentored by you.', status='Pending')

    print("\nDatabase successfully populated!")
    print("==============================")
    print("Login Credentials:")
    print("Admin:   admin    | admin123")
    print("Student: student1 | password123")
    print("Alumni:  alumni1  | password123")
    print("Alumni:  alumni2  | password123 (unverified)")

if __name__ == '__main__':
    populate()
