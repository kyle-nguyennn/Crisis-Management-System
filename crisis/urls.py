from django.conf.urls import url

from crisis import views

app_name = 'crisis'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register')
]
