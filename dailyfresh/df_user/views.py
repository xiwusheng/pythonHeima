# coding=utf-8
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse

from hashlib import sha1

from django.http import JsonResponse
from . import user_decorator
from django.core.paginator import Paginator

from models import *
from df_order.models import *

# Create your views here.


def index(request):
    return HttpResponse('<h1>Index page of User</h1>')


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
            # 此处的url是user_decorator.py中预先存入的，便于返回之前未登陆的页面。如果没有就使用/
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


def logout(request):
    request.session.flush()
    return redirect('/')


def register_exist(request):
    uname = request.GET.get('uname')

    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})
    # two line for test
    # context = {'count': count}
    # return render(request, 'df_user/debug.html', context)


@user_decorator.login
def info(request):  # 用户中心

    user_email = UserInfo.objects.get(id=request.session.get('user_id')).uemail

    # 最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_ids1 = goods_ids.split(',')
    goods_list = []

    if goods_ids1:
        for goods_id in goods_ids1:
            # 如果goods_ids1为空时，下一行有bug。todo
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))
            explain = '最近浏览'
    else:
        explain = '无最近浏览'

    context = {
        'title': '用户中心',
        'user_email': user_email,
        'user_name': request.session.get('user_name'),
        'page_name': 1,
        'goods_list': goods_list,
        'explain': explain,
    }

    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def order(request, index):
    user_id = request.session['user_id']
    orders_list = OrderInfo.objects.filter(ouser_id=int(user_id)).order_by('-odate')
    paginator = Paginator(orders_list, 2)
    page = paginator.page(int(index))
    context = {
        'paginator': paginator,
        'page': page,
        'orders_list': orders_list,
        'title': "用户中心",
        'page_name': 1,
    }

    return render(request, 'df_user/user_center_order.html', context)


@user_decorator.login
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



