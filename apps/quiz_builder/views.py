from django import forms
import django
from django.contrib.auth import authenticate, login
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import (View, TemplateView)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apps.content_management.models import StructuredEnglishGrammarCourse
from apps.quiz_builder.forms.formulario_quiz_builder import app
7

@login_required(login_url='login')
def quiz_builder_home(request):
    return render(request, 'quiz_builder/quiz_builder_home.html', {'current_pages': ['quiz_builder_home', 'quiz_builder_home']})


@login_required(login_url='login')
def new_quiz(request,pk):

    user = User.objects.get(username=request.user.username)
    screen_width = request.COOKIES.get('screen_width')
    if screen_width is not None:
        screen_width = int(screen_width)

    request.session['language'] = request.POST.get('language', 'English')


    context = {
     #   'post': post,
        'user_id' : user.id,
        'username': user.username,
        'screen_width': screen_width,
        'current_page': 'request_form',
        'select_form': 'Formulario_Quiz_Builder',  # Agrega select_form al contexto
    }
    
    
    if pk == 8:
        print('OCHO')
        return render(request, 'quiz_builder/quiz_builder_home.html', context)
        #return render(request, 'request/new_request.html', {'user_id' : user.id, 'username': request.user.username, 'selected_language':get_context(request)})
    else:
        return render(request, 'formularios/formulario_no_disponible.html', context)
    