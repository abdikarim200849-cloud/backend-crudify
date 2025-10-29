from django.urls import path
from . import views

urlpatterns = [
    path("", views.student_list, name="student_list"),
    path('add/', views.add_student, name='add_student'),
    path('<int:id>/edit/', views.edit_student, name='edit_student'),
    path('add-group/', views.add_group, name='add_group'),
    path('add-club/', views.add_club, name='add_club'),
    path('<int:id>/delete/', views.delete_student, name='delete_student'),
    path('<int:id>/', views.student_detail, name='student_detail'),
    path('<int:id>/delete_photo/', views.delete_photo, name='delete_photo'),
]