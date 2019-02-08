from datetime import datetime
import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django_redis import get_redis_connection

from db.base_view import VerifyLoginView
from goods.models import GoodsSKU
from orders.models import Transport, Order, OrderGoods
from shopping.hepler import get_cart_key, json_msg
from users.models import UserAddress, Users


class TureorderView(VerifyLoginView):
    '''
    确认订单
    '''

    def get(self, request):
        '''
         有地址或者有默认地址时
         地址为空时显示
        '''
        # 地址处理
        user_id = request.session.get('ID')
        address = UserAddress.objects.filter(user_id=user_id).order_by('-isDefault').first()
        # address = None
        '''
         展示商品信息
        '''
        # # 利用redis获取数量
        # # redis
        # r = get_redis_connection()
        # # 准备键
        # user_id = request.session.get("ID")
        # cart_key = f"shopcart_{user_id}"
        # # 获取
        # values = r.hgetall(cart_key)
        # # print(values)  # {b'1': b'22', b'4': b'31', b'2': b'4', b'3': b'1'}
        # # 获取商品总价格
        # # 准备一个空列表,保存多个商品
        # goods_skus = []
        # # 遍历字典
        # for pk, counts in values.items():
        #     pk = int(pk)
        #     counts = int(counts)
        #
        #     # 根据购物中的sku_id从 商品sku表中获取商品信息
        #     try:
        #         goods_sku = GoodsSKU.objects.get(pk=pk, is_delete=False, is_on_sale=True)
        #     except GoodsSKU.DoesNotExist:
        #         continue
        #
        #     # 将购物车中数量和商品信息合成一块儿(给一个已经存在的对象添加属性)
        #     goods_sku.count = counts
        #     # setattr(goods_sku,'count',count)
        #
        #     # 保存商品到商品列表
        #     goods_skus.append(goods_sku)

        # 处理商品信息
        sku_ids = request.GET.getlist("sku_ids")
        # 准备空列表 装商品
        goods_skus = []
        # 准备商品总计
        goods_total_price = 0

        # 准备redis
        r = get_redis_connection()
        # 准备键
        cart_key = get_cart_key(user_id)

        # 遍历
        for sku_id in sku_ids:
            # 商品信息
            try:
                goods_sku = GoodsSKU.objects.get(pk=sku_id)
            except GoodsSKU.DoesNotExist:
                # 商品不存在就回到购物车
                # return HttpResponse('1')
                return redirect("shopping:购物车")
            # 获取对应商品的数量
            try:
                count = r.hget(cart_key, sku_id)
                count = int(count)
            except:
                # 商品不存在就回到购物车
                # return HttpResponse('2')
                return redirect("shopping:购物车")

            # 保存到商品对象上
            goods_sku.count = count

            # 装商品
            goods_skus.append(goods_sku)

            # 统计商品总计
            goods_total_price += goods_sku.price * count

            # 获取运输方式
            transports = Transport.objects.filter(is_delete=False).order_by('price')

        context = {
            'address': address,
            'goods_sku': goods_skus,
            'goods_total_price': goods_total_price,
            'transports':transports,
        }
        return render(request, 'orders/tureorder.html', context=context)

    def post(self, request):
        """
                   保存订单数据
                   1. 订单基本信息表 和 订单商品表
               """

        # # 1. 接收参数
        transport_id = request.POST.get('transport')
        sku_ids = request.POST.getlist('sku_ids')
        address_id = request.POST.get('address')

        # 接收用户的id
        user_id = request.session.get("ID")
        user = Users.objects.get(pk=user_id)

        # 验证数据的合法性
        try:
            transport_id = int(transport_id)
            address_id = int(address_id)
            sku_ids = [int(i) for i in sku_ids]
        except:
            return JsonResponse(json_msg(2, "参数错误!"))

        # 验证收货地址和运输方式存在
        try:
            address = UserAddress.objects.get(pk=address_id)
        except UserAddress.DoesNotExist:
            return JsonResponse(json_msg(3, "收货地址不存在!"))

        try:
            transport = Transport.objects.get(pk=transport_id)
        except Transport.DoesNotExist:
            return JsonResponse(json_msg(4, "运输方式不存在!"))

        # 2. 操作数据

        # >>>1 . 操作订单基本信息表
        order_sn = "{}{}{}".format(datetime.now().strftime("%Y%m%d%H%M%S"), user_id, random.randrange(10000, 99999))
        address_info = "{}{}{}-{}".format(address.hcity, address.hproper, address.harea, address.brief)
        order = Order.objects.create(
            user=user,
            order_sn=order_sn,
            transport_price=transport.price,
            transport=transport.name,
            username=address.username,
            phone=address.phone,
            address=address_info
        )

        # >>>2. 操作订单商品表
        # 操作redis
        r = get_redis_connection()
        cart_key = get_cart_key(user_id)

        # 准备个变量保存商品总金额
        goods_total_price = 0

        for sku_id in sku_ids:

            # 获取商品对象
            try:
                goods_sku = GoodsSKU.objects.get(pk=sku_id, is_delete=False, is_on_sale=True)
            except GoodsSKU.DoesNotExist:
                return JsonResponse(json_msg(5, "商品不存在"))

            # 获取购物车中商品的数量
            # redis 基于内存的存储,有可能数据会丢失
            try:
                count = r.hget(cart_key, sku_id)
                count = int(count)
            except:
                return JsonResponse(json_msg(6, "购物车中数量不存在!"))

            # 判断库存是否足够
            if goods_sku.stock < count:
                return JsonResponse(json_msg(7, "库存不足!"))

            # 保存订单商品表
            order_goods = OrderGoods.objects.create(
                order=order,
                goods_sku=goods_sku,
                price=goods_sku.price,
                count=count
            )

            # 添加商品总金额
            goods_total_price += goods_sku.price * count

            # 扣除库存, 销量增加
            goods_sku.stock -= count
            goods_sku.sale_num += count
            goods_sku.save()

        # 3. 反过头来操作订单基本信息表 商品总金额 和 订单总金额
        # 订单总金额
        order_price = goods_total_price + transport.price
        order.goods_total_price = goods_total_price
        order.order_price = order_price
        order.save()

        # 4. 清空redis中的购物车数据(对应sku_id)
        r.hdel(cart_key, *sku_ids)

        # 3. 合成响应
        return JsonResponse(json_msg(0, "创建订单成功!", data=order_sn))
        # return HttpResponse('ok')

class OrderView(VerifyLoginView):
    '''
    确认支付
    '''

    def get(self, request):
        # 接收用户id
        user_id = request.session.get("ID")
        # 接收order_sn
        order_sn = request.GET.get("order_sn")

        try:
            order = Order.objects.get(order_sn=order_sn, user_id=user_id)
        except Order.DoesNotExist:
            return redirect("shopping:购物车")

        # 计算订单总金额
        total = order.transport_price
        # 渲染订单到页面
        context = {
            "order": order,
            "total": total,
        }
        return render(request, 'orders/order.html', context=context)

    def post(self, request):
        pass
