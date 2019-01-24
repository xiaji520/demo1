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

    def get(self, request):
        # 查询所有的分类
        category = Category.objects.filter(is_delete=False)
        # 查询所有的商品
        goods_sku = GoodsSKU.objects.filter(is_delete=False)

        context = {
            'category': category,
            'goods_sku': goods_sku,
        }
        return render(request, 'goods/category.html', context=context)

    def post(self, request):
        pass
