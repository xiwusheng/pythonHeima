# coding=utf-8

from django.http import JsonResponse
from .models import *
from df_user import user_decorator
from django.shortcuts import render, redirect

# Create your views here.


@user_decorator.login
def cart(request):
    uid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=uid)
    context = {
        'title': '购物车',
        'page_name': 1,
        'carts': carts,
    }

    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        # 求当前用户购买了几个商品
        return JsonResponse({'count': count})
    else:
        return render(request, 'df_cart/cart.html', context)


@user_decorator.login
def add(request, gid, count):
    uid = request.session['user_id']
    gid, count = int(gid), int(count)
    # 查询购物车中是否已经有此物品，如果有则数量增加，没有则新增
    carts = CartInfo.objects.filter(user_id=uid, goods_id=gid)

    if len(carts) >= 1:
        cart = carts[0]
        cart.count = cart.count + count
    else:
        cart = CartInfo()
        cart.user_id = uid
        cart.goods_id = gid
        cart.count = count
    cart.save()

    # 如果是ajax提交，直接返回json，否则转向购物车
    if request.is_ajax():
        count = CartInfo.objects.filter(user_id=request.session['user_id']).count()
        # 当前用户购买了几个商品
        return JsonResponse({'count': count})
    else:
        return redirect('/cart/')


@user_decorator.login
def edit(request, cart_id, count):
    data = {}
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.count = int(count)
        cart.save()
        data['count'] = 0
    except Exception:
        data['count'] = count
    return JsonResponse(data)


@user_decorator.login
def delete(request, cart_id):
    data = {}
    try:
        cart = CartInfo.objects.get(pk=int(cart_id))
        cart.delete()
        data['ok'] = 1
    except Exception:
        data['ok'] = 0
    return JsonResponse(data)


