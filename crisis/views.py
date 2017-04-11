import sys

import json

from django.contrib.auth.models import User
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from django.core import serializers

from crisis.dao import CaseDao
from crisis.caseManager import CaseManager
from crisis.models import MyUser, Case, Subscriber
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
    template_name = 'crisis/report_incident.html'

    # display blank form
    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    # process form data
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            print("form is valid")
            case = form.save()
            # cleaned data
        else:
            print("form is not fucking valid")
            return HttpResponse({"status": "failed"})

        return HttpResponse(request)

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
                context = {'username': user.username}
                return redirect('crisis:index')
                #return render(request, '/crisis/index.html', context)
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
    if request.user.is_authenticated():
        user = request.user
        if user.userType == 0:
            return redirect('crisis:dashboard')
        else:
            return redirect('crisis:relevant_agency')
    return render(request, 'crisis/index.html')


def dashboard(request):
    if request.user.is_authenticated():
        usertype = request.user.userType
        if usertype == 0:
            return render(request, 'crisis/dashboard.html')
        else:
            return redirect('crisis:index')
    return redirect('crisis:index')

def relevant_agency(request):
    return render(request, 'crisis/relevant_agency.html')

def summary(request):
    if request.user.is_authenticated():
        user = request.user
        userType = user.userType
        if userType == 0:
            summary = {}
            summary["active"] = CaseManager.getActive()
            summary["resolved"] = CaseManager.getResolved()
            summary["total"] = CaseManager.getTotal()
            summary["crisislevel"] = CaseManager.getCrisisLevel()
            print(summary)
            return HttpResponse(json.dumps(summary), content_type='json')
        return HttpResponse({})
    else:
        return HttpResponse({})


def get_cases(request):
    if request.user.is_authenticated():
        user = request.user
        userType = user.userType
        print(userType)
        cases = CaseDao.getByUserType(userType)
    else:
        cases = CaseDao.getActiveCase()
    data = serializers.serialize('json', cases,
                                     fields=('pk', 'longitude', 'latitude', 'category', 'status', 'detail', 'place_name'))
    return HttpResponse(data, content_type='json')

def new_case(request):
    if request.user is not None:
        user = request.user
        userType = user.userType
        if userType == 0:
            if request.method == "POST":
                case = Case(
                    name=request.POST['name'],
                    phoneNum=request.POST['phoneNum'],
                    gender=request.POST['gender'],
                    ic=request.POST['ic'],
                    longitude=request.POST['longitude'],
                    latitude=request.POST['latitude'],
                    category=request.POST['category'],
                    detail=request.POST['detail'],
                    place_name=request.POST['place_name'],
                    region=request.POST['region']
                )
                # case={}
                # case['name'] = request.POST['name']
                # case['phoneNum'] = request.POST['phoneNum']
                # case['gender'] = request.POST['gender']
                # case['ic'] = request.POST['ic']
                # case['longitude'] = request.POST['longitude']
                # case['latitude'] = request.POST['latitude']
                # case['category'] = request.POST['category']
                # case['detail'] = request.POST['detail']
                # case['place_name'] = request.POST['place_name']
                # case['region'] = request.POST['region']
                # case = Case(case)
                case.save()
                return redirect('crisis:dashboard')
            else:
                return render(request, 'crisis/report_incident.html', {})
        else:
            return HttpResponse(json.dumps({'status': 'no authority'}), content_type='json')
    else:
        return HttpResponse(json.dumps({'status':'no user'}), content_type='json')

def change_case_status(request):
    if request.user.is_authenticated():
        user = MyUser.objects.filter(username=request.user.username)
        if user.userType != 1:
            caseId = request.POST['pk']
            newStatus = request.POST['status']
            if CaseDao.upDateStatus(CaseDao(), user.userType, caseId, newStatus): #update success:
                return HttpResponse(json.dumps({'status', 'success'}), content_type='json')
            else:
                return HttpResponse(json.dumps({'status', 'user not authenticated to change this entry'}),
                                    content_type='json')
        else:
            return HttpResponse(json.dumps({'status', 'Call Operator is not authorised to change this entry'}),
                                content_type='json')
    return None

def validate(request):
    if request.user.is_authenticated():
        usertype = request.user.userType
        print(request.POST)
        pk = request.POST['pk']
        valid = int(request.POST['valid'])
        newStatus = -1
        if valid == 1:
            print('inside check')
            newStatus = 1
        elif valid == 0:
            newStatus = 2
        if newStatus != -1:
            if CaseDao.upDateStatus(usertype, pk, newStatus):
                return HttpResponse({'success':'Update status successfully'})
        return HttpResponse({'error':'Invalid input'})
    else:
        return HttpResponse({'error':'You are not authorised to perform this action'})

def resolve(request):
    if request.user.is_authenticated():
        usertype = request.user.userType
        pk = request.POST['pk']
        severity = request.POST['severity']
        dead = request.POST['dead']
        injured = request.POST['injured']
        if CaseDao.updateSeverity(usertype, pk, severity):
            if CaseDao.updateDead(usertype, pk, dead):
                if CaseDao.updateInjured(usertype, pk, injured):
                    CaseDao.upDateStatus(usertype, pk, 2)
                    return HttpResponse({
                        'success': 'Update case information successfully'})
        return HttpResponse({'error': 'Invalid input'})
    else:
        return HttpResponse({'error': 'You are not authorised to perform this action'})

def subscribe(request):

    if request.method=='GET':
        return render(request, 'crisis/subscribe.html')
    elif request.method=='POST':
        categoryList = request.POST.getlist("category")
        for x in categoryList:
            subscriber = Subscriber(
                phoneNum = request.POST["phoneNum"],
                category = x,
                region = request.POST['region']
            )
            subscriber.save()
        return redirect('crisis:index')
    return HttpResponse(request)

def unsubscribe(request):
    return render(request, 'crisis/unsubscribe.html')

def changeSubscription(request):
    return render(request, 'crisis/changeSubscription.html')

def reportToGovernment(request):
    print(request.path)
    if (str(request.path).__contains__('government')):
        return render(request, 'crisis/government_report.html')
    if (str(request.path).__contains__('case')):
        #temporarily not handling this
        return render(request, 'crisis/government_report.html')

    if (str(request.path).__contains__('category')):
        result = CaseManager.countCaseGroupByCategory()
        return HttpResponse(json.dumps(result), content_type='json')

    if (str(request.path).__contains__('injured')):
        result = CaseManager.countInjuredGroupByCategory()
        print(result)
        return HttpResponse(json.dumps(result), content_type='json')
    if (str(request.path).__contains__('dead')):
        result = CaseManager.countDeadGroupByCategory()
        return HttpResponse(json.dumps(result), content_type='json')
    return None

def test(request):
    return render(request, 'crisis/test.html', {})


