import sys

import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.core import serializers

from crisis.caseDao import CaseDao
from crisis.models import MyUser, CaseStatus, UserType, Case
from crisis.serializer import CaseSerializer
from .forms import UserForm, CaseForm


# Create your views here.

class UserFormView(View):
    form_class = UserForm
    template_name = 'crisis/registration_form.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # cleaned data
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.userType = UserType.CivilDefense.value
            user.save()
            # user = User.objects.get(username=username)
            # data = {'username':username, 'status':'testing'}
            # return HttpResponse(json.dumps(data), content_type='application/json')

            # returns User objects if credentials are correct
            return redirect('crisis:login')
        return render(request, self.template_name, {'form': form})

class CaseFormView(View):
    form_class = CaseForm
    template_name = 'crisis/new_case_2.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            case = form.save(commit=False)
            # cleaned data


        return HttpResponse({})

def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                user = request.user
                context = {'user': user}
                return render(request, 'crisis/index.html', context)
                #inside index.html, there is a js script with AJAX call to 'crisis:index'
                #to get what cases should be fetched from server
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
        context = {'user': user}
        userType = user.userType
        #cases = CaseDao.getByUserType(userType)
        cases = Case.objects.all()
        print(cases)
        data = serializers.serialize('json', cases)
        return HttpResponse(data, content_type='application/json')
    return render(request, 'crisis/index.html', context)

def new_case(request):
    context = {}
    if request.user is not None:
        if request.method == "POST":
            return HttpResponse(json.dumps(request.POST), content_type='application/json')
        else:
            return render(request, 'crisis/new_case.html', {})
    else:
        return HttpResponse(json.dumps({'status':'no user'}), content_type='application/json')

def test(request):
    return render(request, 'crisis/test.html', {})
