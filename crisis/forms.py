from django.contrib.auth.models import User
from django import forms

from crisis.models import Case, MyUser


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password']

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['name', 'phoneNum', 'gender', 'ic', 'longitude', 'latitude', 'category', 'detail']