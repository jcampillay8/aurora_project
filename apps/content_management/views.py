from django import forms
import django
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.shortcuts import render, get_object_or_404
from apps.quiz_builder.models import CourseLessonQuiz
from apps.content_management.english_models.English_Writing.app import app
from django.contrib.auth.models import User
from django.conf import settings

def starter(request):
    return render(request, 'courses/choose_level.html')

@login_required(login_url='login')
def starter_home(request):
    return render(request, 'courses/starter_home.html', {'current_pages': ['starter_home', 'starter_home']})

@login_required(login_url='login')
def a1_home(request):
    return render(request, 'courses/a1_home.html', {'current_pages': ['a1_home', 'a1_home']})

@login_required(login_url='login')
def a2_home(request):
    return render(request, 'courses/a2_home.html', {'current_pages': ['a2_home', 'a2_home']})

@login_required(login_url='login')
def b1_home(request):
    return render(request, 'courses/b1_home.html', {'current_pages': ['b1_home', 'b1_home']})

@login_required(login_url='login')
def b2_home(request):
    return render(request, 'courses/b2_home.html', {'current_pages': ['b2_home', 'b2_home']})

@login_required(login_url='login')
def lesson_details(request, course_level, categoria_lesson):
    lessons = CourseLessonQuiz.objects.filter(Course_Level=course_level, Categoria_Lesson=categoria_lesson)
    print(lessons)
    return render(request, 'courses/lesson_details.html', {'lessons': lessons, 'course_level': course_level, 'categoria_lesson': categoria_lesson})



@login_required(login_url='login')
def course_detail(request, lesson_id):
    user = request.user
    screen_width = request.COOKIES.get('screen_width', 1024)  # Asignar un valor por defecto si no está presente
    screen_width = int(screen_width)

    selected_quiz = get_object_or_404(CourseLessonQuiz, id=lesson_id)

    context = {
        'user_id': user.id,
        'username': user.username,
        'screen_width': screen_width,
        'select_quiz': selected_quiz,  # Añadir el quiz seleccionado al contexto
    }

    return render(request, 'courses/course_detail.html', context)