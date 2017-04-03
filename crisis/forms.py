from django.contrib.auth.models import User
from django import forms

from crisis.models import Case


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['longitude', 'latitude', 'category']