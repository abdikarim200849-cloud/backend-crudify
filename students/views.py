from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Student
from .forms import StudentForm
from django.contrib.auth.models import User
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from .models import Student, Group, Club
from django import forms
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Student
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Список студентов с поиском, фильтрацией и сортировкой
@login_required
def student_list(request):
    query = request.GET.get('q')
    group_filter = request.GET.get('group')
    club_filter = request.GET.get('club')
    sort_by = request.GET.get('sort')

    students = Student.objects.select_related('group').prefetch_related('clubs').all()

    if query:
        students = students.filter(
            Q(first_name__icontains=query) | Q(last_name__icontains=query)
        )

    if group_filter:
        students = students.filter(group__name__icontains=group_filter)

    if club_filter:
        students = students.filter(clubs__name__icontains=club_filter)
    
    if club_filter:
        students = students.filter(clubs__name__icontains=club_filter)



    if sort_by in ['age', 'first_name', 'last_name']:
        students = students.order_by(sort_by)
    elif sort_by == 'group':
        students = students.order_by('group__name')

    return render(request, "students/index.html", {
        "students": students,
        "query": query,
        "group_filter": group_filter,
        "club_filter": club_filter,
        "sort_by": sort_by
    })

# Добавление студентов
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль студента успешно добавлен!")
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'students/add.html', {'form': form})

# Редактирование студента
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, request.FILES, instance=student)  
        if form.is_valid():
            form.save()
            messages.success(request, "Профиль студента успешно обновлён!")
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'students/edit.html', {'form': form})

# Удаление студента
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Профиль студента успешно удалён!")
        return redirect('student_list')
    return render(request, 'students/delete.html', {'student': student})

# Просмотр деталей студента
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, "students/detail.html", {"student": student})

# Удаление фотографии студента
def delete_photo(request, id):
    student = get_object_or_404(Student, id=id)
    if student.photo:
        student.photo.delete()
        student.photo = None
        student.save()
    return redirect('edit_student', id=id)

# Регистрация пользователя
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password1"]
            if User.objects.filter(username=username).exists():
                form.add_error("username", "Пользователь с таким именем уже существует.")
            elif User.objects.filter(email=email).exists():
                form.add_error("email", "Email уже используется.")
            else:
                User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, "Регистрация прошла успешно!")
                return redirect("login")
    else:
        form = RegisterForm()
    return render(request, "students/register.html", {"form": form})

# Логин пользователя
def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            if username and password:
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Вы успешно вошли!")
                    return redirect("student_list")
                else:
                    form.add_error(None, "Неверные данные для входа.")
    else:
        form = LoginForm()

    return render(request, "students/login.html", {"form": form})

def logout_view(request):
    logout(request)
    messages.success(request, "Вы вышли из аккаунта.")
    return redirect("login")

#Добавление групп и клубов
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'curator']

class ClubForm(forms.ModelForm):
    class Meta:
        model = Club
        fields = ['name']

@login_required
def add_group(request):
    form = GroupForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Группа добавлена!")
        return redirect('add_student') 
    return render(request, 'students/group.html', {'form': form})

@login_required
def add_club(request):
    form = ClubForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Клуб добавлен!")
        return redirect('add_student')
    return render(request, 'students/club.html', {'form': form})