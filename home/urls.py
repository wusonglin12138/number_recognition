from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^upload/$', views.upload),
    url(r'^pre_conduct/$', views.preconduct),
    # url(r'^result/$', views.test),
    url(r'^detail/pid=(\d+)', views.detail),
    url(r'^manage/uid=(\d*)/page=(\d*)', views.manage),
    url(r'^help', views.helper),

    # url(r'^save_picture', views.save_picure)
]