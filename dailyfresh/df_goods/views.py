# coding=utf-8
from django.shortcuts import render
from django.core.paginator import Paginator

# from df_user.models import UserInfo
from df_cart.models import CartInfo
from .models import GoodsInfo, TypeInfo


# Create your views here.


def index(request):
    # 查询各个分类的最新4条数据
    typelist = TypeInfo.objects.all()

    type0 = typelist[0].goodsinfo_set.order_by('-id')[0:4]  # 按照上传顺序
    tpye01 = typelist[0].goodsinfo_set.order_by('-gclick')[0:4]  # 按照点击量
    type1 = typelist[1].goodsinfo_set.order_by('-id')[0:4]
    tpye11 = typelist[1].goodsinfo_set.order_by('-gclick')[0:4]
    type2 = typelist[2].goodsinfo_set.order_by('-id')[0:4]
    tpye21 = typelist[2].goodsinfo_set.order_by('-gclick')[0:4]
    type3 = typelist[3].goodsinfo_set.order_by('-id')[0:4]
    tpye31 = typelist[3].goodsinfo_set.order_by('-gclick')[0:4]
    type4 = typelist[4].goodsinfo_set.order_by('-id')[0:4]
    tpye41 = typelist[4].goodsinfo_set.order_by('-gclick')[0:4]
    type5 = typelist[5].goodsinfo_set.order_by('-id')[0:4]
    tpye51 = typelist[5].goodsinfo_set.order_by('-gclick')[0:4]

    cart_num = 0
    # 判断是否存在登陆状态
    # if request.session.has_key('user_id'):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    context = {
        'title': '首页',
        'guest_cart': 1,
        'cart_num': cart_num,
        # 'type0': type0, 'type01': type01,
        # 'type1': type0, 'type11': type11,
        # 'type2': type0, 'type21': type21,
        # 'type3': type0, 'type31': type31,
        # 'type4': type0, 'type41': type41,
        # 'type5': type0, 'type51': type51,

    }

    return render(request, 'df_goods/index.html', context)


def good_list(request, tid, pindex, sort):
    # tid：商品种类信息  pindex：商品页码 sort：商品显示分类方式
    typeinfo = TypeInfo.objects.get(pk=int(tid))

    # 根据主键查找当前的商品分类  海鲜或者水果
    news = typeinfo.goodsinfo_set.order_by('-id')[0:2]
    # list.html左侧最新商品推荐
    goods_list = []
    # list中间栏商品显示方式
    cart_num, guest_cart = 0, 0

    try:
        user_id = request.session['user_id']
    except:
        user_id = None
    if user_id:
        guest_cart = 1
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    if sort == '1':  # 默认最新
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-id')
    elif sort == '2':  # 按照价格
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gprice')
    elif sort == '3':  # 按照人气点击量
        goods_list = GoodsInfo.objects.filter(gtype_id=int(tid)).order_by('-gclick')

    # 创建Paginator一个分页对象
    paginator = Paginator(goods_list, 4)
    # 返回Page对象，包含商品信息
    page = paginator.page(int(pindex))
    context = {
        'title': '商品列表',
        'guest_cart': guest_cart,
        'cart_num': cart_num,
        'page': page,
        'paginator': paginator,
        'typeinfo': typeinfo,
        'sort': sort,  # 排序方式
        'news': news,
    }
    return render(request, 'df_goods/list.html', context)


def detail(request, gid):
    good_id = gid
    goods = GoodsInfo.objects.get(pk=int(good_id))
    goods.gclick = goods.gclick + 1  # 商品点击量
    goods.save()

    news = goods.gtype.goodsinfo_set.order_by('-id')[0:2]

    cart_num = 0
    # 判断是否存在登陆状态
    # if request.session.has_key('user_id'):
    if 'user_id' in request.session:
        user_id = request.session['user_id']
        cart_num = CartInfo.objects.filter(user_id=int(user_id)).count()

    # cart_num 传给html中我的购物车旁边显示的数量，调用view.py cart_count方法
    context = {
        'title': goods.gtype.ttitle,
        'guest_cart': 1,
        'cart_num': cart_num,
        'goods': goods,
        'news': news,
        'id': good_id,
    }
    response = render(request, 'df_goods/detail.html', context)

    # if 'user_id' in request.session:
    #     user_id = request.session["user_id"]
    #     try:
    #         browsed_good = GoodsBrowser.objects.get(user_id=int(user_id), good_id=int(good_id))
    #     except Exception:
    #         browsed_good = None
    #     if browsed_good:
    #         from datetime import datetime
    #         browsed_good.browser_time = datetime.now()
    #         browsed_good.save()
    #     else:
    #         GoodsBrowser.objects.create(user_id=int(user_id), good_id=int(good_id))
    #         browsed_goods = GoodsBrowser.objects.filter(user_id=int(user_id))
    #         browsed_good_count = browsed_goods.count()
    #         if browsed_good_count > 5:
    #             ordered_goods = browsed_goods.order_by("-browser_time")
    #             for _ in ordered_goods[5:]:
    #                 _.delete()

    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id = '%d'%goods.id

    if goods_ids != '':  # 判断是否有浏览记录，如果有则继续判断
        goods_ids1 = goods_ids.split(',')
        if goods_ids1.count(goods_id) >= 1:
            goods_ids1.remove(goods_id)
        goods_ids1.insert(0, goods_id)
        if len(goods_ids1) >= 6:
            del goods_ids1[5]
        goods_ids = ','.join(goods_ids1)
    else:
        goods_ids = goods_id
    response.set_cookie('goods_ids', goods_ids)

    return response


# 顶部我的购物车显示的数量
def cart_count(request):
    if 'user_id' in request.session:
        return CartInfo.objects.filter(user_id=request.session['user_id']).count()
    else:
        return 0






