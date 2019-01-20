from django.conf.urls import url

from users.views import register, login

urlpatterns = [
    url(r'^register$',register,name='注册'),
    url(r'^login$',login,name='登录'),
]
