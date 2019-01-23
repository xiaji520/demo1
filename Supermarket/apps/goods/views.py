from django.shortcuts import render

# Create your views here.
from django.views import View


class IndexView(View):
    '''
    主页
    '''

    def get(self, request):
        pass
        return render(request, 'goods/index.html')

    def post(self, request):
        pass


class DetailView(View):
    '''
    商品详情
    '''

    def get(self, request):
        pass
        return render(request, 'goods/detail.html')

    def post(self, request):
        pass


class CategoryView(View):
    '''
    商品列表
    '''

    def get(self, request):
        pass
        return render(request, 'goods/category.html')

    def post(self, request):
        pass


