from django.contrib import admin
# Register your models here.
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from crisis.models import *


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ('id', 'longitude', 'latitude', 'category', 'status')


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    list_display = ('username', 'userType')
    fieldsets = UserAdmin.fieldsets + (
            (None, {'fields': ('userType',)}),
    )


admin.site.register(MyUser, MyUserAdmin)
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('pk','phoneNum', 'category', 'region')
