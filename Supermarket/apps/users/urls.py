from django.conf.urls import url

from users.views import RegisterView, LoginView, InforView, ForgetView, PasswordView, SendMsg, MemberView, AddressView, \
    GladdressView

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='注册'),
    url(r'^login/$', LoginView.as_view(), name='登录'),
    url(r'^infor/$', InforView.as_view(), name='个人资料'),
    url(r'^forgetpassword/$', ForgetView.as_view(), name='忘记密码'),
    url(r'^password/$', PasswordView.as_view(), name='修改密码'),
    url(r'^sendmsg/$', SendMsg.as_view(), name='发送短信验证'),
    url(r'^member/$', MemberView.as_view(), name='个人中心'),
    url(r'^address/$', AddressView.as_view(), name='收货地址'),
    url(r'^gladdress/$', GladdressView.as_view(), name='管理收货地址'),
    # url(r'^village/$', VillageView.as_view(), name='校区选择'),
]
