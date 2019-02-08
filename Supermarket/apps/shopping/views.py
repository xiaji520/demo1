from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection

from db.base_view import VerifyLoginView
from goods.models import GoodsSKU
from shopping.hepler import json_msg, get_shopcart_count


class AddShopcartView(VerifyLoginView):
    '''
    操作购物车, 添加购物车数据
    '''

    """
        1. 需要接收的参数
            sku_id count 
            从session中获取用户id

        2. 验证参数合法性
            a. 判断 为整数
            b. 要在数据库中存在商品
            c. 验证库存是否充足

        3. 操作数据库
            将购物车 保存到redis
            存储的时候采用的数据类型为hash
            key           field value  field value
            cart_user_id  sku_id       count

    """

    def post(self, request):
        # 接受参数
        user_id = request.session.get('ID')
        sku_id = request.POST.get('sku_id')
        count = request.POST.get('count')

        # 1.判断是否为整数
        try:
            sku_id = int(sku_id)
            count = int(count)
        except:
            return JsonResponse(json_msg(1, '参数错误!'))
        # 2.在数据库中存商品
        try:
            goods_sku = GoodsSKU.objects.get(pk=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse(json_msg(2, '商品不存在!'))

        # 3.判断库存
        if goods_sku.stock < count:
            return JsonResponse(json_msg(3, '库存不足!'))

        # 操作数据库
        # 创建连接
        r = get_redis_connection()
        # 处理购物车的 键
        shopcart_key = f"shopcart_{user_id}"

        # 添加
        # 获取购物车中存在的数量 加上需要添加 与库存进行比较
        old_count = r.hget(shopcart_key, sku_id)  # 注意格式,二进制
        if old_count is None:
            old_count = 0
        else:
            old_count = int(old_count)  # 转码

        if goods_sku.stock < old_count + count:
            return JsonResponse(json_msg(3, '库存不足!'))

        # 添加商品到购物车
        # r.hget(shopcart_key, sku_id, count + old_count)
        rs_count = r.hincrby(shopcart_key, sku_id, count)  # 可以自增自减
        if rs_count <= 0:
            # 删除为0的商品
            r.hdel(shopcart_key, sku_id)

        # 获取购物车中的总数量
        cart_count = get_shopcart_count(request)

        return JsonResponse(json_msg(0, '添加购物车成功!', data=cart_count))


class ShopcartListView(VerifyLoginView):
    '''
    购物车
    '''

    def get(self, request):
        # 利用redis获取数量
        # redis
        r = get_redis_connection()
        # 准备键
        user_id = request.session.get("ID")
        cart_key = f"shopcart_{user_id}"
        # 获取
        values = r.hgetall(cart_key)
        # print(values)  # {b'1': b'22', b'4': b'31', b'2': b'4', b'3': b'1'}
        # 获取商品总价格
        # 准备一个空列表,保存多个商品
        goods_skus = []
        # 遍历字典
        for pk, counts in values.items():
            pk = int(pk)
            counts = int(counts)

            # 根据购物中的sku_id从 商品sku表中获取商品信息
            try:
                goods_sku = GoodsSKU.objects.get(pk=pk, is_delete=False, is_on_sale=True)
            except GoodsSKU.DoesNotExist:
                # 删除redis过期数据
                r.hdel(cart_key,pk)
                continue

            # 将购物车中数量和商品信息合成一块儿(给一个已经存在的对象添加属性)
            goods_sku.count = counts
            # setattr(goods_sku,'count',count)

            # 保存商品到商品列表
            goods_skus.append(goods_sku)

        context = {
            'goods_sku': goods_skus,

        }
        return render(request, 'shopping/shopcart.html', context=context)

    def post(self, request):
        pass


class AllorderView(VerifyLoginView):
    '''
    订单页
    '''

    def get(self, request):
        return render(request, 'shopping/allorder.html')

    def post(self, request):
        pass



