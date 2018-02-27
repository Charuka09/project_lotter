from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    url(r'^$', views.index, name='index'),
    url(r'^login$', auth_views.login, name='login'),

    url(r'^logout$', auth_views.logout, {'next_page': 'login'}, name='logout'),

    url(r'^projects/(?P<pid>\d+)/enrollments/(?P<status>[^/]+)$', views.modify_enrollments),
    url(r'^draws/(?P<draw_id>\d+)/start$', views.start_project_draw),
    url(r'^all_projects', views.all_projects, name='all_projects'),
]