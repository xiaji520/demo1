from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection

from db.base_view import VerifyLoginView
from goods.models import GoodsSKU


class OrderView(VerifyLoginView):
    '''
    订单
    '''


    def get(self, request):
        # 查询所有的商品
        goods_sku = GoodsSKU.objects.filter(is_delete=False)
        # 利用redis获取数量
        # redis
        r = get_redis_connection()
        # 准备键
        user_id = request.session.get("ID")
        cart_key = f"shopcart_{user_id}"
        # 获取
        values = r.hgetall(cart_key)
        # print(values)  # {b'1': b'22', b'4': b'31', b'2': b'4', b'3': b'1'}
        # 字典推导式获取商品总价格
        goods = {GoodsSKU.objects.get(pk=int(pk)): int(counts) for pk, counts in values.items()}
        # print(goods)
        # 获取各个商品总价,返回列表
        price_list = [sku.price * count for sku, count in goods.items()]
        # print(price_list)
        price = 0
        for p in price_list:
            price += p
            # print(price)
        context = {
            'goods_sku': goods_sku,
            'price': price,
        }
        return render(request, 'orders/order.html',context=context)

    def post(self, request):
        pass