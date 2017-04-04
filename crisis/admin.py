from django.contrib import admin

# Register your models here.
from crisis.models import Case, MyUser

admin.site.register(Case)
admin.site.register(MyUser)
