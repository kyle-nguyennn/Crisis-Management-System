import sys

import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.core import serializers

from crisis import caseDao
from crisis.caseDao import CaseDao
from crisis.models import MyUser, Case
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
            user.username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.userType = form.cleaned_data['userType']
            user.set_password(password)
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
        print("this is post")
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            print("user is not none")
            if user.is_active:
                login(request, user)
                user = request.user
                context = {'user': user}
                return render(request, '../index.html', context)
                #inside index.html, there is a js script with AJAX call to 'crisis:index'
                #to get what cases should be fetched from server
            else:
                return render(request, 'crisis/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'crisis/login.html', {'error_message:': 'Invalid login!!!'})
    else:
        print("this is GET  ")
    return render(request, 'crisis/login.html')

def logout_user(request):
    logout(request)
    return render(request, 'crisis/login.html')

def index(request):
    return render(request, 'crisis/index.html')

def get_cases(request):
    if request.user.is_authenticated():
        user = request.user
        userType = user.userType
        print(userType)
        cases = CaseDao.getByUserType(CaseDao(), userType)
        data = serializers.serialize('json', cases,
                                     fields=('pk', 'longitude', 'latitude', 'category', 'status', 'detail'))
        return HttpResponse(data, content_type='application/json')
    else:
        return None

def new_case(request):
    context = {}
    if request.user is not None:
        if request.method == "POST":
            return HttpResponse(json.dumps(request.POST), content_type='application/json')
        else:
            return render(request, 'crisis/new_case.html', {})
    else:
        return HttpResponse(json.dumps({'status':'no user'}), content_type='application/json')

def change_case_status(request):
    if request.user.is_authenticated():
        user = MyUser.objects.filter(username=request.user.username)
        if user.userType != 1:
            caseId = request.POST['pk']
            newStatus = request.POST['status']
            if CaseDao.upDateStatus(user.userType, caseId, newStatus): #update success:
                return HttpResponse(json.dumps({'status', 'success'}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status', 'user not authenticated to change this entry'}),
                                    content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status', 'Call Operator is not authorised to change this entry'}),
                                content_type='application/json')
    return None

def update_severity(request):
    return None

def update_dead(request):
    return None

def update_injuries(request):
    return None

def subscribe(request):
    return render(request, 'crisis/subscribe.html')

def unsubscribe(request):
    return render(request, 'crisis/unsubscribe.html')

def changeSubscription(request):
    return render(request, 'crisis/changeSubscription.html')

def test(request):
    return render(request, 'crisis/test.html', {})


