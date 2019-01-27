from django.conf.urls import url

from shopping.views import ShopcartListView, AllorderView, TureorderView, AddShopcartView

urlpatterns = [
    url(r'^addshopcart/$', AddShopcartView.as_view(), name='添加购物车'),
    url(r'^shopcartlist/$', ShopcartListView.as_view(), name='购物车'),
    url(r'^allorder/$', AllorderView.as_view(), name='订单页'),
    url(r'^tureorder/$', TureorderView.as_view(), name='确认订单'),
]
