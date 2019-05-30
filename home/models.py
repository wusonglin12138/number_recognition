from django.db import models
from user.models import UserInfo


class PictureInfo(models.Model):
    pcreatetime = models.DateTimeField()
    purl = models.CharField(max_length=100)
    pstatus = models.CharField(max_length=1)
    puser = models.ForeignKey(UserInfo)
    pretime = models.FloatField()
    preresult = models.CharField(max_length=1)
    prepercent_0 = models.FloatField()
    prepercent_1 = models.FloatField()
    prepercent_2 = models.FloatField()
    prepercent_3 = models.FloatField()
    prepercent_4 = models.FloatField()
    prepercent_5 = models.FloatField()
    prepercent_6 = models.FloatField()
    prepercent_7 = models.FloatField()
    prepercent_8 = models.FloatField()
    prepercent_9 = models.FloatField()

