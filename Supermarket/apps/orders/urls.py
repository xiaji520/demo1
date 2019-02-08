from django.conf.urls import url

from orders.views import OrderView, TureorderView

urlpatterns = [
    url(r'^order/$', OrderView.as_view(), name='确认支付'),
    url(r'^tureorder/$', TureorderView.as_view(), name='确认订单'),
]
