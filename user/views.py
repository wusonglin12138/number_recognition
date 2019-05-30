# coding=utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from .models import *
from hashlib import sha1
from django.utils import timezone
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import random
import os


def register(request):
    return render(request, 'user/register.html')


def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post.get('username').encode('utf-8')
    upwd = post.get('password')
    upwd2 = post.get('confirm_password')
    ugender = post.get('gender')
    uemail = post.get('email')
    ucontact = post.get('phone')
    uicon = '/static/images/picture/profile.png'
    # print("------=====")
    # print("uname charset is: " + chardet.detect(uname))

    # 判断两次密码
    if upwd != upwd2:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd.encode("utf-8"))
    upwd3 = s1.hexdigest()

    # 创建模型类对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.ugender = ugender
    user.ucontact = ucontact
    user.uemail = uemail
    user.uicon = uicon
    # 设置时间
    ISOTIMEFORMAT = '%Y - %m - %d % X'
    user.ulogintime = timezone.now()
    user.uposition = '0'
    user.save()

    # 注册成功，转到登陆页面
    return redirect('/user/login/')


def register_exist(request):
    uname = request.GET.get('uname')
    # print("-------")
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')

    context = {'error_name': 0, 'uname': uname}
    return render(request, 'user/login.html', context)


def login_handle(request):
    post = request.POST
    uname = post.get('username')
    upwd = post.get('password')
    remember = post.get('remember', 0)

    users = UserInfo.objects.filter(uname=uname)
    # print(type(users[0].id))

    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode("utf-8"))
        if s1.hexdigest() == users[0].upwd:
            # print(users[0].upwd)
            red = HttpResponseRedirect('/home')
            if remember != 0:
                red.set_cookie('uname', uname)
                # print(uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = str(users[0].id)
            request.session['user_name'] = uname
            request.session['user_email'] = users[0].uemail
            request.session['user_position'] = users[0].uposition
            request.session['user_icon'] = users[0].uicon
            # red['title'] = 'Home'

            # create picture dir
            pic_dir = '/home/tf/hdidentify/static/images/picture/' + str(users[0].id) + '/'
            if os.path.exists(pic_dir) is False:
                os.makedirs(pic_dir)
            return red
        else:
            context = {'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'user/login.html', context)
    else:
        context = {'error_name': 1, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
        return render(request, 'user/login.html', context)


def forgot(request):
    return render(request, 'user/forgot.html')


def forgot_handle(request):
    uname1 = request.GET.get('uname')
    uemail1 = request.GET.get('uemail')
    # ver_code = request.POST.get('ver_code')
    users = UserInfo.objects.filter(uname=uname1)
    if len(users) == 1:
        if users[0].uemail != uemail1:
            return JsonResponse({'error_name': 0, 'error_email': 1, 'uname': uname1})
        else:
            int_list = [random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9)]
            str_list = ""
            for i in int_list:
                str_list += str(i)
            request.session['ver_code'] = str_list
            sender = 'wusonglin12138@126.com'
            receivers = uemail1
            text = "Mnist试验站验证码:" + str_list
            print(text)
            message = MIMEText(text, 'plain', 'utf-8')
            message['Subject'] = Header('Mnist试验站验证码', 'utf-8')
            message['From'] = 'wsl'+'<wusonglin12138@126.com>'
            message['To'] = '' + '<' + uemail1 + '>'
            smtp = smtplib.SMTP('localhost')
            smtp.connect('smtp.126.com')
            smtp.login('wusonglin12138@126.com', 'wsl83918543')
            # # smtp.send_message(message, sender, receivers)
            smtp.sendmail(sender, receivers, message.as_string())
            smtp.quit()
            return HttpResponse()
    else:
        return JsonResponse({'error_name': 1, 'error_email': 0})


def forgot_check_ver_code(request):
    ver_code = request.POST.get('ver_code')
    uname = request.POST.get('username')
    uemail = request.POST.get('email')
    if ver_code == request.session.get('ver_code'):
        context = {'uname': uname}
        return render(request, 'user/confirm.html', context)
    else:
        context = {'uemail': uemail, 'uname': uname, 'error_ver_code': 1}
        return render(request, 'user/forgot.html', context)


def forgot_reset(request):
    upwd = request.POST.get('password')
    uname = request.POST.get('uname')
    s1 = sha1()
    s1.update(upwd.encode("utf-8"))
    UserInfo.objects.filter(uname=uname).update(upwd=s1.hexdigest())
    # print(uname)
    context = {'uname': uname, 'upwd': upwd}
    return render(request, 'user/login.html', context)


def profile(request, uid, modify):
    user = UserInfo.objects.filter(id=uid)
    user_id = user[0].id
    user_name = user[0].uname
    gender = user[0].ugender
    last_login_time = user[0].ulogintime
    contact = user[0].ucontact
    email = user[0].uemail
    position = user[0].uposition
    icon = user[0].uicon
    if position == '1':
        position = 'Administrator'
    else:
        position = 'Normal User'

    context = {'user_id': user_id, 'user_name': user_name, 'user_gender': gender, 'user_last_login_time': last_login_time,
               'user_contact': contact, 'user_email': email, 'user_position': position, 'user_icon': icon}
    if modify == '1':
        html = 'user/profile_modify.html'
    else:
        html = 'user/profile.html'
    return render(request, html, context)


def profile_modify(request):
    user_id = request.POST.get('user_id')
    user_name = request.POST.get('user_name')
    contact = request.POST.get('contact')
    email = request.POST.get('email')
    print(user_id)
    file = request.FILES.get('icon', None)

    base_dir = '/home/tf/hdidentify'
    search_dict = dict()
    if file:
        icon_dir = '/static/images/picture/' + user_id + '/' + file.name

        destination = open(base_dir + icon_dir, 'wb+')
        for chunk in file.chunks():
            destination.write(chunk)
        destination.close()
        search_dict['uicon'] = icon_dir
        request.session['user_icon'] = icon_dir

    UserInfo.objects.filter(id=user_id).update(ucontact=contact, uemail=email, **search_dict)
    request.session['user_email'] = email

    return HttpResponseRedirect('/home')
