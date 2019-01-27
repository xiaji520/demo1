from django.conf.urls import url

from orders.views import OrderView

urlpatterns = [
    url(r'^order/$', OrderView.as_view(), name='订单'),
]
