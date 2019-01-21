from django.conf.urls import url

from users.views import RegisterView, LoginView, InforView, ForgetView, PasswordView

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='注册'),
    url(r'^login/$', LoginView.as_view(), name='登录'),
    url(r'^infor/$', InforView.as_view(), name='个人资料'),
    url(r'^forgetpassword/$', ForgetView.as_view(), name='忘记密码'),
    url(r'^password/$', PasswordView.as_view(), name='修改密码'),
]
