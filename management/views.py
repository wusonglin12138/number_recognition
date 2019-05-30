from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from home.models import PictureInfo
from user.models import UserInfo
from django.http.response import JsonResponse
from home.paginator import Paginator
import datetime
import time
import json
from django.forms.models import model_to_dict
from django.db import connection


@csrf_exempt
def user_manage(request):

    def time_splits(times, num):
        # print(times)
        if times != "" and times != 'None':
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
            timestamp = time.mktime(
                datetime.datetime(int(year), int(month), int(day), int(hour), int(minute), 0).timetuple())
            # return {'year': year, 'month': month, 'day': day, 'hour': hour, 'minute': minute}
            return timestamp
        else:
            timestamp = time.mktime(datetime.datetime(1970, 1, 1, 0, 0, 0).timetuple())
            # return {'year': '1900', 'month': '01', 'day': '01', 'hour': '00', 'minute': '00'}
            return timestamp

    if request.method == 'POST':
        user_id = request.POST.get("user_id")
        user_name = request.POST.get("user_name")
        from_time = request.POST.get("from")
        to_time = request.POST.get("to")
        image_status = request.POST.get("image_status")
        pindex = request.POST.get("pindex")
        if pindex == "":
            pindex = '1'

        from_time_timestamp = time_splits(from_time, 1)
        to_time_timestamp = time_splits(to_time, 2)

        search_dict = dict()
        picture_list = []
        user_list = []
        # pictures = []   # 暂存记录
        if user_id:
            search_dict['puser_id'] = user_id
        if user_name:
            search_dict['puser_id__uname__icontains'] = user_name
        if image_status:
            search_dict['pstatus'] = image_status

        picture = PictureInfo.objects.filter(**search_dict)

        # print(management_info)
        for pic in picture:
            user = pic.puser
            user_list.append(model_to_dict(user))
            timestamp = time.mktime(
                datetime.datetime(pic.pcreatetime.year, pic.pcreatetime.month, pic.pcreatetime.day,
                                  pic.pcreatetime.hour, pic.pcreatetime.minute, 0).timetuple())
            if from_time_timestamp <= timestamp <= to_time_timestamp:
                picture_list.append(pic)
        # print(user_list)
        # print(picture_list)
        paginator = Paginator(picture_list, 10, int(pindex))
        page_num = paginator.page_num()
        page_index_num = paginator.page_index_num()
        page_json_list = paginator.page()
        print(page_json_list)
        context = {'page_num': page_num, 'page_index_num': page_index_num, 'page': page_json_list, 'pindex': pindex,
                   'from_time': from_time, 'to_time': to_time, 'image_status': image_status}
        # print(context)
        return JsonResponse(json.dumps(context), safe=False)
    else:
        return render(request, 'manage/admin_user_management.html', {'title': 'User Management'})


@csrf_exempt
def delete_picture(request):
    picture_id = request.POST.get('id')

    picture = PictureInfo.objects.get(id=picture_id)
    picture.pstatus = '0'
    picture.save()
    context = {'isDelete': 1}
    return JsonResponse(json.dumps(context), safe=False)


