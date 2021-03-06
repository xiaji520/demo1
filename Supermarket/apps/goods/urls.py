from django.conf.urls import url

from goods.views import IndexView, CategoryView, DetailView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='首页'),
    url(r'^list/(?P<cate_id>\d*)_{1}(?P<order>\d?)\.html$', CategoryView.as_view(), name='商品列表'),
    url(r'^detail/(?P<id>\d+)/$', DetailView.as_view(), name='商品详情'),
]
