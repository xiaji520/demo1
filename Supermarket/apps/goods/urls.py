from django.conf.urls import url

from goods.views import IndexView, CategoryView, DetailView

urlpatterns = [
    url(r'^index/$', IndexView.as_view(), name='首页'),
    url(r'^detail/$', DetailView.as_view(), name='商品详情'),
    url(r'^category/$', CategoryView.as_view(), name='商品列表'),
]
