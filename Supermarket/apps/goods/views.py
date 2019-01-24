from django.shortcuts import render

# Create your views here.
from django.views import View

from goods.models import GoodsSPU, Banner, GoodsSKU, Category


class IndexView(View):
    '''
    主页
    '''

    def get(self, request):
        # 获取轮播
        banner = Banner.objects.all()
        # 查询所有的商品
        goods_sku = GoodsSKU.objects.filter(is_delete=False)
        context = {
            'banner': banner,
            'goods_sku': goods_sku,
        }
        return render(request, 'goods/index.html', context=context)


def post(self, request):
    pass


class DetailView(View):
    '''
    商品详情
    '''

    def get(self, request, id):
        # 获取商品sku信息
        goods_sku = GoodsSKU.objects.get(pk=id)
        context = {
            'goods_sku': goods_sku,
        }
        return render(request, 'goods/detail.html', context=context)

    def post(self, request, id):
        pass


class CategoryView(View):
    '''
    商品分类
    '''
    """
   1. 页面刚加载的时候 显示的商品只 显示 排序 排第一的分类下的商品
   2. 点击哪个分类 就显示 对应分类下的商品
   3. 可以按照 销量,价格(降,升),添加时间,综合(pk) 排序 并且 是对应分类下的商品
    添加一个参数order: 
                0: 综合
                1: 销量降
                2: 价格升
                3: 价格降
                4: 添加时间降
            order_rule = ['pk', '-sale_num', 'price', '-price', '-create_time']
    """

    def get(self, request, cate_id,order):
        # 查询所有的分类
        categorys = Category.objects.filter(is_delete=False).order_by("-order")
        # 取出第一个分类
        # print(categorys.first())

        if cate_id == "":
            category = categorys.first()
            cate_id = category.pk
        else:
            # 根据分类id查询对应的分类
            cate_id = int(cate_id)
            try:  # 判断参数是否超出范围,超出范围返回第一页
                category = Category.objects.get(pk=cate_id)
            except:
                category = categorys.first()

        # 查询所有的商品
        goods_sku = GoodsSKU.objects.filter(is_delete=False, category=category)
        if order == '':
            order = 0
        order = int(order)

        # 排序规则列表
        order_rule = ['pk', '-sale_num', 'price', '-price', '-create_time']
        # 判断参数是否超出范围,超出范围返回综合排序
        count=0
        for _ in order_rule:
            count+=1
        if count < order:
            order=1
            goods_sku = goods_sku.order_by(order_rule[order])

        context = {
            'category': categorys,
            'goods_sku': goods_sku,
            'cate_id': cate_id,
            'order': order,
        }
        return render(request, 'goods/category.html', context=context)

    def post(self, request, cate_id,order):
        pass
