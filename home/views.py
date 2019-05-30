# coding=utf-8
from django.shortcuts import render
import datetime
import time
from .models import UserInfo
from .models import PictureInfo
from django.utils import timezone
from .predict import Predict
from django.views.decorators.csrf import csrf_exempt
import base64
from django.http import JsonResponse
import json
from .paginator import Paginator
import random


def index(request):
    user_id = request.session.get('user_id')
    if request.session.get('user_position') == "1":
        # print(request.session.get('user_position'))
        return render(request, 'manage/overview.html', {'user_id': user_id, 'title': 'Home', 'color':'0'})
    else:
        return render(request, 'home/index.html', {'user_id': user_id, 'title': 'Home', 'color':'0'})


def upload(request):

    if request.session.get('user_id') is None:

        return render(request, 'user/login.html')
    else:
        return render(request, 'home/upload.html', {'title': 'Laboratory', 'color':'1'})


@csrf_exempt
def preconduct(request):
    if request.method == "POST":
        isdraw = request.POST.get('isDraw')
        file = request.FILES.get('upload', None)
        id = request.session.get('user_id')

        time = timezone.now()
        if isdraw == '1':
            imagedata = request.POST.get('imageData')
            file = base64.b64decode(imagedata)
            filename = str(random.randint(0, 9)) + '.png'
            print(filename)
        else:
            filename = file.name
        # 上传图片
        Basedir = id + '/' + str(time.year) + str(time.month) + str(time.day) + str(time.hour) + \
                  str(time.minute) + str(time.second) + '_' + filename
        basedir = '/home/tf/hdidentify/static/images/picture/' + Basedir
        print(basedir)
        destination = open(basedir, 'wb+')

        if isdraw == "1":
            destination.write(file)
            destination.close()
        else:
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()

        picture_url = '/static/images/picture/' + Basedir

        # predict
        pred = Predict(basedir)
        # pred.img_dir = basedir
        result, result_probability, time_cross = pred.predict()

        # save to database
        picture = PictureInfo()

        picture.pcreatetime = time
        picture.preresult = result[0]
        picture.pstatus = '1'
        picture.pretime = round(time_cross, 2)
        picture.purl = picture_url
        picture.puser = UserInfo.objects.filter(id=request.session.get('user_id'))[0]
        picture.prepercent_0 = result_probability[0][0]
        picture.prepercent_1 = result_probability[0][1]
        picture.prepercent_2 = result_probability[0][2]
        picture.prepercent_3 = result_probability[0][3]
        picture.prepercent_4 = result_probability[0][4]
        picture.prepercent_5 = result_probability[0][5]
        picture.prepercent_6 = result_probability[0][6]
        picture.prepercent_7 = result_probability[0][7]
        picture.prepercent_8 = result_probability[0][8]
        picture.prepercent_9 = result_probability[0][9]
        picture.save()
        # print("------id="+str(picture.id))
        print("-------------")
        print(result[0])
        context = {'result': str(result[0]), 'pid': picture.id, 'picture_url': picture_url, 'title': 'Laboratory', 'color':'1'}
        print(context)
        if isdraw == "1":
            return JsonResponse(json.dumps(context), safe=False)
        else:
            return render(request, 'home/result.html', context)
    else:
        pid = request.GET.get("pid")
        result = request.GET.get("result")
        title = request.GET.get("title")
        context = {'result': result, 'pid': pid, 'title': title}
        return render(request, 'home/result.html', context)



# def save_picure(request):
#     imagedata = request.POST.get('imageData')
#     imageData64 = base64.b64encode(imagedata)
#     time = timezone.now()
#
#     Basedir = id + '/' + str(time.year) + str(time.month) + str(time.day) + str(time.hour) + \
#               str(time.minute) + str(time.second) + '_' + id + '.png'
#     basedir = '/home/tf/hdidentify/static/images/picture/' + Basedir
#
#
#     return render(request, 'home/result.html')


def detail(request, pid):
    picture = PictureInfo.objects.filter(id=pid)
    pid = picture[0].id
    pcreatetime = picture[0].pcreatetime
    preresult = picture[0].preresult
    prepercent_0 = picture[0].prepercent_0
    prepercent_1 = picture[0].prepercent_1
    prepercent_2 = picture[0].prepercent_2
    prepercent_3 = picture[0].prepercent_3
    prepercent_4 = picture[0].prepercent_4
    prepercent_5 = picture[0].prepercent_5
    prepercent_6 = picture[0].prepercent_6
    prepercent_7 = picture[0].prepercent_7
    prepercent_8 = picture[0].prepercent_8
    prepercent_9 = picture[0].prepercent_9

    context = {'id': pid, 'pcreatetime': pcreatetime,'preresult': preresult, 'prepercent_0': round(prepercent_0, 4)*100,
               'prepercent_1': round(prepercent_1*100, 4), 'prepercent_2': round(prepercent_2*100, 4),
               'prepercent_3': round(prepercent_3*100, 4), 'prepercent_4': round(prepercent_4*100, 4),
               'prepercent_5': round(prepercent_5*100, 4), 'prepercent_6': round(prepercent_6*100, 4),
               'prepercent_7': round(prepercent_7*100, 4), 'prepercent_8': round(prepercent_8*100, 4),
               'prepercent_9': round(prepercent_9*100, 4), 'title': 'Laboratory', 'color':'1'}
    return render(request, 'home/detail.html', context)


@csrf_exempt
def manage(request, uid, pindex):
    if request.session.get('user_id') is None:
        return render(request, 'user/login.html')
    else:
        if pindex == '':
            pindex = '1'
        from_time = ""
        to_time = ""
        is_ajax = 0
        picture_list = PictureInfo.objects.filter(puser_id=uid, pstatus='1')

        def time_splits(times, num):
            if times is not None and times != 'None':
                datetimee = times.split('T')
                date = datetimee[0].split('-')
                timee = datetimee[1].split(':')
                year = int(date[0])
                month = int(date[1])
                day = int(date[2])
                hour = int(timee[0])
                minute = int(timee[1])
                timestamp = time.mktime(datetime.datetime(year, month, day, hour, minute, 0).timetuple())
                # time_dic = {'year': year, 'month': month, 'day': day, 'hour': hour, 'minute': minute}
                return timestamp
            elif num == 2:
                year = time.strftime('%Y', time.localtime(time.time()))
                month = time.strftime('%m', time.localtime(time.time()))
                day = time.strftime('%d', time.localtime(time.time()))
                hour = time.strftime('%H', time.localtime(time.time()))
                minute = time.strftime('%M', time.localtime(time.time()))
                timestamp = time.mktime(datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), 0).timetuple())
                # return {'year': year, 'month': month, 'day': day, 'hour': hour, 'minute': minute}
                return timestamp
            else:
                timestamp = time.mktime(datetime.datetime(1970, 1, 1, 0, 0, 0).timetuple())
                # return {'year': '1900', 'month': '01', 'day': '01', 'hour': '00', 'minute': '00'}
                return timestamp
        if request.method == "POST":
            # 搜索
            if request.POST.get('from') != "" or request.POST.get('to') != "":
                from_time = request.POST.get('from')
                to_time = request.POST.get('to')
                is_ajax = 1
                print(from_time)

                from_time_timestamp = time_splits(from_time, 1)

                to_time_timestamp = time_splits(to_time, 2)

                picture = PictureInfo.objects.filter(puser_id=uid, pstatus='1')
                print(type(picture[0].pcreatetime))
                picture_list = []
                # print(from_time_dic['day'])
                for pic in picture:
                    timestamp = time.mktime(
                        datetime.datetime(pic.pcreatetime.year, pic.pcreatetime.month, pic.pcreatetime.day,
                                          pic.pcreatetime.hour, pic.pcreatetime.minute, 0).timetuple())
                    if from_time_timestamp <= timestamp <= to_time_timestamp:
                        picture_list.append(pic)
                # print(len(picture_list))

            paginator = Paginator(picture_list, 10, int(pindex))
            page_num = paginator.page_num()
            page_index_num = paginator.page_index_num()
            page_json_list = paginator.page()
            # print(page_json_list)
            # print(pindex)
            context = {'page_num': page_num, 'page_index_num': page_index_num, 'page': page_json_list, 'pindex': pindex, 'from_time': from_time,
                       'to_time': to_time, 'is_ajax': is_ajax}
            # if is_ajax == 0:
            #     return render(request, 'home/manage.html', context)
            # else:
            #     return render(request, 'home/manage.html', context)
            return JsonResponse(json.dumps(context), safe=False)
        return render(request, 'home/manage.html', {'title': 'Management', 'color':'2'})


def helper(request):
    return render(request, 'home/help.html', {'title': 'Help', 'color':'4'})
