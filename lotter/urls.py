from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [

    url(r'^$', auth_views.login),
    url(r'^login$', auth_views.login, name='login'),

    url(r'index$', views.index, name='index'),

    url(r'^logout$', auth_views.logout, {'next_page': 'login'}, name='logout'),

    url(r'^draws/(?P<draw_id>\d+)/(?P<status>[^/]+)$', views.add_enrollment),

]