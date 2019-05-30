from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user_manage', views.user_manage),
    url(r'^delete_picture/$', views.delete_picture),

]