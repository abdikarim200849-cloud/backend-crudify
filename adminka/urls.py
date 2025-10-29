from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.urls import include
from django.contrib import admin
from students import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('add/', views.add_student, name='add_student'),
    path('add-group/', views.add_group, name='add_group'),
    path('add-club/', views.add_club, name='add_club'),
    path("", lambda request: redirect("student_list"), name="home"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    path("students/", include("students.urls")),
    path("admin/", admin.site.urls), 
    path('add/', views.add_student, name='add_student'),  
    path('<int:id>/edit/', views.edit_student, name='edit_student'),  
    path('<int:id>/delete/', views.delete_student, name='delete_student'),  
    path('<int:id>/', views.student_detail, name='student_detail'),  
    path('<int:id>/delete_photo/', views.delete_photo, name='delete_photo'),  
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)