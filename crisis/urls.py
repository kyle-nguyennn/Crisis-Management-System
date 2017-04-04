from django.conf.urls import url

from crisis import views

app_name = 'crisis'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^test/$', views.test, name='test'),
    url(r'^new_case/$', views.CaseFormView.as_view(), name='new_case'),
]
