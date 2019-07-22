# coding=utf-8
from django.shortcuts import render, redirect, HttpResponseRedirect,HttpResponse
from models import *
from hashlib import sha1
from django.http import JsonResponse

# Create your views here.


def index(request):
    return HttpResponse('<h1>Index page</h1>')


def register(request):

    # 此数值传过去,会放在标签页的位置上
    context = {
        'title': '用户注册YL'
    }
    return render(request, 'df_user/register.html', context)


def register_handle(request):
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2= post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码一致性
    if upwd!=upwd2:
        return redirect('/user/register/')

    # 密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()

    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    # 注册成功，转到登陆界面
    return redirect('/user/login/')


def login(request):

    uname = request.COOKIES.get('uname', '')
    context = {
        'title': '用户登陆',
        'error_name': 0,
        'error_pwd': 0,
        'uname': uname,
    }
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    # 接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu=post.get('jizhu', 0)

    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)

    # 判断用户密码并跳转
    if len(users) != 0:
        # user name founded 111
        s1 = sha1()
        s1.update(upwd)

        if s1.hexdigest() == users[0].upwd:
            # password right 222
            # todo redirect to /user/info/
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)
            # whether checked remember user name 333
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)  # cookie 立刻过期

            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red

        else:
            # password false 222
            context = {
                'title': '用户名登陆',
                'error_name': 0,
                'error_pwd': 1,
                'uname': uname,
                'upwd': upwd,
            }
            return render(request, 'df_user/login.html', context)

    else:
        # user name not exist 111
        context = {
            'title': '用户名登陆',
            'error_name': 1,
            'error_pwd': 0,
            'uname': uname,
            'upwd': upwd,
        }
        return render(request, 'df_user/login.html', context)





def register_exist(request):
    uname = request.GET.get('uname')

    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})
    # two line for test
    # context = {'count': count}
    # return render(request, 'df_user/debug.html', context)


def info(request): # 用户中心
    username = request.session.get('username')
    # user_email = UserInfo.objects.get(id=request.session.get['user_id']).uemail

    context = {
        'title': '用户中心',

        # 'user_email': user_email,
        'user_name': username,

    }

    return render(request, 'df_user/user_center_info.html', context)


def order(request):
    context = {'title': "用户中心"}
    return render(request, 'df_user/user_center_order.html', context)


def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post=request.POST
        user.ushou=post.get('ushou')
        user.uaddress=post.get('uaddress')
        user.uyoubian=post.get('uyoubian')
        user.uphone=post.get('uphone')
        user.save()

    context = {'title': "用户中心", 'user': user}
    return render(request, 'df_user/user_center_site.html', context)


