from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_choices_view, name='login'),
    path('login/student/', views.student_login_view, name='student_login'),
    path('login/alumni/', views.alumni_login_view, name='alumni_login'),
    path('login/admin/', views.admin_login_view, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),
    path('dashboard/alumni/', views.alumni_dashboard, name='alumni_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    
    path('request/send/<int:alumni_id>/', views.send_mentorship_request, name='send_request'),
    path('request/handle/<int:req_id>/<str:action>/', views.handle_request, name='handle_request'),
    path('alumni/verify/<int:alumni_id>/', views.verify_alumni, name='verify_alumni'),
    path('alumni/reject/<int:alumni_id>/', views.reject_alumni, name='reject_alumni'),
    path('student/verify/<int:student_id>/', views.verify_student, name='verify_student'),
    path('student/reject/<int:student_id>/', views.reject_student, name='reject_student'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('chat/', views.chat_inbox, name='chat_inbox'),
    path('chat/<str:target_username>/', views.chat_thread, name='chat_thread'),
]
