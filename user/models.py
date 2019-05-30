from django.db import models


class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    ugender = models.CharField(max_length=6)
    ulogintime = models.DateTimeField()
    ucontact = models.CharField(max_length=11)
    uemail = models.CharField(max_length=20)
    uposition = models.CharField(max_length=1)
    uicon = models.CharField(max_length=100)
