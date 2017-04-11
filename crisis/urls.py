from django.conf.urls import url

from crisis import views

app_name = 'crisis'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^relevant_agency/$', views.relevant_agency, name='relevant_agency'),
    url(r'^summary/$', views.summary, name='summary'),
    url(r'^get_cases/$', views.get_cases, name='get_cases'),
    url(r'^register/$', views.UserFormView.as_view(), name='register'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^test/$', views.test, name='test'),
    url(r'^new_case/$', views.new_case, name='new_case'),
    url(r'^validate/$', views.validate, name='validate'),
    url(r'^resolve/$', views.resolve, name='resolve'),
    # url(r'^change_case_status/$', views.change_case_status, name='change_case_status'),
    # url(r'^update_severity/$', views.update_severity, name='update_severity'),
    # url(r'^update_dead/$', views.update_dead, name='update_dead'),
    # url(r'^update_injuries/$', views.update_injuries, name='update_injuries'),
    url(r'^subscribe/$', views.subscribe, name='subscribe'),
    url(r'^unsubscribe/$', views.unsubscribe, name='unsubscribe'),
    url(r'^changeSubscription/$', views.changeSubscription, name='changeSubscription'),
    url(r'^government_report/$', views.reportToGovernment, name='governementReport'),
    url(r'^number_by_category/$', views.reportToGovernment, name='number_by_category'),
    url(r'^number_of_injured/$', views.reportToGovernment, name='number_of_injured'),
    url(r'^number_of_dead/$', views.reportToGovernment, name='number_of_dead'),
    url(r'^haze/*$', views.getHaze, name='haze'),
]
