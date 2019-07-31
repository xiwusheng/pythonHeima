# coding=utf-8
from django.shortcuts import render, HttpResponse
from django.db import transaction
from django.http import JsonResponse

from datetime import datetime
from decimal import Decimal

from df_user.models import UserInfo
from df_cart.models import *
from df_user import user_decorator
from .models import OrderInfo, OrderDetailInfo

# Create your views here.


@user_decorator.login
def order(request):
    uid = request.session['user_id']
    user = UserInfo.objects.get(id=uid)
    cart_ids = request.GET.getlist('cart_id')
    carts = []
    total_price = 0
    for goods_id in cart_ids:
        cart = CartInfo.objects.get(id=goods_id)
        carts.append(cart)
        total_price = total_price + float(cart.count) * float(cart.goods.gprice)

    total_price = float('%0.2f' % total_price)
    trans_cost = 10
    total_trans_price = trans_cost + total_price
    context = {
        'title': '提交订单',
        'page_name': 1,
        'user': user,
        'carts': carts,
        'total_price': float('%0.2f' % total_price),
        'trans_cost': trans_cost,
        'total_trans_price': total_trans_price,
    }

    return render(request, 'df_order/place_order.html', context)


@user_decorator.login
@transaction.atomic()  # 事务
def order_handle(request):
    tran_id = transaction.savepoint()
    # 接收购物车编号
    cart_ids = request.POST.get('cart_ids')  # 购物车，此时cart_ids为字符串，例如'1,2,3,'
    user_id = request.session['user_id']
    data = {}

    try:
        order_info = OrderInfo()
        now = datetime.now()

        order_info.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), user_id)
        order_info.odate = now
        order_info.user_id = int(user_id)
        order_info.ototal = Decimal(request.POST.get('total'))
        order_info.save()

        for cart_id in cart_ids.split(','):
            cart = CartInfo.objects.get(pk=cart_id)
            order_detail = OrderDetailInfo()
            order_detail.order = order_info
            goods = cart.goods
            if cart.count <= goods.gkucun:
                goods.gkucun = goods.gkucun - cart.count
                goods.save()
                order_detail.goods = goods
                order_detail.price = goods.gprice
                order_detail.count = cart.count
                order_detail.save()
                cart.delete()
            else:
                transaction.savepoint_rollback(tran_id)
                return HttpResponse('库存不足')

        data['ok'] = 1
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print("===============%s" % e)
        print('未完成订单提交')
        transaction.savepoint_rollback(tran_id)
    return JsonResponse(data)

# 事务：一旦操作失败则全部回退
# 1. 创建订单对象
# 2. 判断商品的库存
# 3. 创建详单对象
# 4. 修改商品库存
# 5. 删除购物车


@user_decorator.login
def pay(request):
    pass








