from django.conf.urls import url

from orders.views import OrderView, TureorderView, Pay, Notify

urlpatterns = [
    url(r'^order/$', OrderView.as_view(), name='确认支付'),
    url(r'^tureorder/$', TureorderView.as_view(), name='确认订单'),
    url(r'^pay/$', Pay.as_view(), name='支付结果'),
    url(r'^notify/$', Notify.as_view(), name='后台支付通知'),
]
