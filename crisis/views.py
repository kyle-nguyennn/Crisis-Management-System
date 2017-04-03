import sys

import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .forms import UserForm


# Create your views here.

class UserFormView(View):
    form_class = UserForm
    template_name = 'crisis/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # proces form data
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # cleaned data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            # returns User objects if credentials are correct
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('crisis:index')
        return render(request, self.template_name, {'form': form})


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect('crisis:index')
            else:
                return render(request, 'crisis/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'crisis/login.html', {'error_message:': 'Invalid login!!!'})
    return render(request, 'crisis/login.html')

def logout_user(request):
    logout(request)
    return render(request, 'crisis/login.html')


def index(request):
    context = {}
    if request.user.is_authenticated():
        user = request.user
        print(sys.stderr, user.username)
        context = {'user': user}
    return render(request, 'crisis/index.html', context)

def new_case(request):
    context = {}
    if request.user is not None:
        if request.method == "POST":
            return HttpResponse(json.dumps({'status': 'reading new case'}), content_type='application/json')
        else:
            return render(request, 'crisis/new_case.html', {})
    else:
        return HttpResponse(json.dumps({'status':'no user'}), content_type='application/json')

def test(request):
    return render(request, 'crisis/test.html', {})
