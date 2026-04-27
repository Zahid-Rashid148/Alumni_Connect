from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, StudentProfileForm, AlumniProfileForm, PostForm
from .models import User, StudentProfile, AlumniProfile, MentorshipRequest, Post, Event

def home_view(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_student:
                return redirect('student_dashboard')
            elif user.is_alumni:
                return redirect('alumni_dashboard')
            else:
                return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_choices_view(request):
    return render(request, 'login_choices.html')

def student_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if getattr(user, 'is_student', False):
                login(request, user)
                return redirect('student_dashboard')
            else:
                form.add_error(None, "You do not have a Student account.")
    else:
        form = AuthenticationForm()
    return render(request, 'student_login.html', {'form': form})

def alumni_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if getattr(user, 'is_alumni', False):
                login(request, user)
                return redirect('alumni_dashboard')
            else:
                form.add_error(None, "You do not have an Alumni account.")
    else:
        form = AuthenticationForm()
    return render(request, 'alumni_login.html', {'form': form})

def admin_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user.is_superuser:
                login(request, user)
                return redirect('admin_dashboard')
            else:
                form.add_error(None, "You do not have an Administrator account.")
    else:
        form = AuthenticationForm()
    return render(request, 'admin_login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def student_dashboard(request):
    if not request.user.is_student:
        return redirect('home')
    alumni_list = AlumniProfile.objects.filter(is_verified=True)
    posts = Post.objects.all().order_by('-created_at')
    events = Event.objects.all().order_by('-date')
    sent_requests = MentorshipRequest.objects.filter(student=request.user)
    return render(request, 'student_dashboard.html', {
        'alumni_list': alumni_list,
        'posts': posts,
        'events': events,
        'sent_requests': sent_requests
    })

@login_required
def alumni_dashboard(request):
    if not request.user.is_alumni:
        return redirect('home')
    received_requests = MentorshipRequest.objects.filter(alumni=request.user)
    my_posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('alumni_dashboard')
    else:
        post_form = PostForm()

    return render(request, 'alumni_dashboard.html', {
        'received_requests': received_requests,
        'my_posts': my_posts,
        'post_form': post_form
    })

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser:
        return redirect('home')
    students = StudentProfile.objects.all()
    alumnis = AlumniProfile.objects.all()
    posts = Post.objects.all()
    events = Event.objects.all()
    return render(request, 'admin_dashboard.html', {
        'students': students,
        'alumnis': alumnis,
        'posts': posts,
        'events': events,
    })

@login_required
def send_mentorship_request(request, alumni_id):
    if request.user.is_student:
        alumni_user = get_object_or_404(User, id=alumni_id, is_alumni=True)
        MentorshipRequest.objects.get_or_create(student=request.user, alumni=alumni_user)
    return redirect('student_dashboard')

@login_required
def handle_request(request, req_id, action):
    if request.user.is_alumni:
        req = get_object_or_404(MentorshipRequest, id=req_id, alumni=request.user)
        if action == 'accept':
            req.status = 'Accepted'
        elif action == 'reject':
            req.status = 'Rejected'
        req.save()
    return redirect('alumni_dashboard')

@login_required
def verify_alumni(request, alumni_id):
    if request.user.is_superuser:
        alumni_prof = get_object_or_404(AlumniProfile, id=alumni_id)
        alumni_prof.is_verified = True
        alumni_prof.save()
    return redirect('admin_dashboard')

@login_required
def reject_alumni(request, alumni_id):
    if request.user.is_superuser:
        alumni_prof = get_object_or_404(AlumniProfile, id=alumni_id)
        alumni_prof.user.delete()
    return redirect('admin_dashboard')

@login_required
def verify_student(request, student_id):
    if request.user.is_superuser:
        student_prof = get_object_or_404(StudentProfile, id=student_id)
        student_prof.is_verified = True
        student_prof.save()
    return redirect('admin_dashboard')

@login_required
def reject_student(request, student_id):
    if request.user.is_superuser:
        student_prof = get_object_or_404(StudentProfile, id=student_id)
        student_prof.user.delete()
    return redirect('admin_dashboard')

@login_required
def edit_profile_view(request):
    if getattr(request.user, 'is_student', False):
        profile = request.user.student_profile
        from .forms import StudentProfileForm
        form_class = StudentProfileForm
        redirect_to = 'student_dashboard'
    elif getattr(request.user, 'is_alumni', False):
        profile = request.user.alumni_profile
        from .forms import AlumniProfileForm
        form_class = AlumniProfileForm
        redirect_to = 'alumni_dashboard'
    else:
        return redirect('home')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect(redirect_to)
    else:
        form = form_class(instance=profile)
        
    return render(request, 'edit_profile.html', {'form': form})

from django.db.models import Q
from django.http import HttpResponseForbidden
from .models import Message

@login_required
def chat_inbox(request):
    if not (getattr(request.user, 'is_student', False) or getattr(request.user, 'is_alumni', False)):
        return redirect('home')
        
    messages = Message.objects.filter(Q(sender=request.user) | Q(receiver=request.user)).order_by('-timestamp')
    recent_users = []
    seen = set()
    for msg in messages:
        other = msg.receiver if msg.sender == request.user else msg.sender
        if other.id not in seen:
            recent_users.append(other)
            seen.add(other.id)
            
    return render(request, 'chat_inbox.html', {'recent_chats': recent_users})

@login_required
def chat_thread(request, target_username):
    if getattr(request.user, 'is_student', False) and not getattr(request.user.student_profile, 'is_verified', False):
        return HttpResponseForbidden("You must be verified to use the chat.")
    if getattr(request.user, 'is_alumni', False) and not getattr(request.user.alumni_profile, 'is_verified', False):
        return HttpResponseForbidden("You must be verified to use the chat.")

    target_user = get_object_or_404(User, username=target_username)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(sender=request.user, receiver=target_user, content=content)
            return redirect('chat_thread', target_username=target_username)

    chat_messages = Message.objects.filter(
        Q(sender=request.user, receiver=target_user) | 
        Q(sender=target_user, receiver=request.user)
    ).order_by('timestamp')

    return render(request, 'chat_thread.html', {
        'target_user': target_user,
        'chat_messages': chat_messages
    })
