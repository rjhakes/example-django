from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='default'),
    url(r'^index/$', views.index, name='index'),
    url(r'^home/$', views.index, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^grade/([0-9]*)', views.saveGrade, name='grade'),
    #url(r'^grades/$', views.showGrades, name='grades'),
    url(r'^grades/$', views.showGradesUsingTemplate, name='grades'),
    url(r'^students/$', views.allGrades, name='allGrades'),
    url(r'^delete/(?P<student_id>[0-9]+)/$', views.deleteGrade, name='delete'),
    url(r'^addgrade/$', views.saveGrade, name='addGrade'),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^loginProcess/$', views.loginProcess, name='loginProcess'),
]