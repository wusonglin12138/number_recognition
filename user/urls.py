from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register_handle/$', views.register_handle),
    url(r'^register_exist', views.register_exist),
    url(r'^login/$', views.login),
    url(r'^login_handle/$', views.login_handle),
    url(r'^forgot/$', views.forgot),
    url(r'^forgot_handle/', views.forgot_handle),
    url(r'^forgot_check_ver_code/$', views.forgot_check_ver_code),
    url(r'^forgot_reset/$', views.forgot_reset),
    url(r'^profile/uid=(\d+)/modify=(\d)', views.profile),
    url(r'^profile_modify',views.profile_modify),
]
