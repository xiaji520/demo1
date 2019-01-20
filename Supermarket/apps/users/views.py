import hashlib

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from users.forms import RegisterForm, LoginForm
from users.models import Users


class IndexView(View):
    '''
    首页
    '''

    def get(self, request):
        return render(request, "users/index.html")



class RegisterView(View):
    '''
    注册视图
    '''
    template_name = 'users/reg.html'

    def get(self, request):
        # 展示登录表单
        return render(request, self.template_name)

    def post(self, request):
        # 完成用户信息的注册
        # 接收参数
        data = request.POST
        # 验证参数合法性 表单验证
        form = RegisterForm(data)
        if form.is_valid():
            # 获取清洗后的数据
            cleaned = form.cleaned_data
            # 将密码进行加密
            # 取出清洗后的手机号
            mobile = cleaned.get('mobile')
            # 取出清洗后的密码
            password = cleaned.get('password')
            h = hashlib.md5(password.encode("utf-8"))  # 将传入的密码进行md5加密
            password = h.hexdigest()
            # print(name,password)
            # 修改到数据库
            data = {'mobile': mobile,
                    'password': password}
            Users.objects.create(**data)
            # 跳转到登录页
            return redirect('users:登录')
        else:
            # 错误
            return render(request, self.template_name, context={'errors': form.errors, })


class LoginView(View):
    """登录视图"""

    def get(self, request):
        return render(request, 'users/login.html')

    def post(self, request):
        # 接收参数
        data = request.POST

        # 验证数据的合法性
        form = LoginForm(data)
        if form.is_valid():
            ################
            # session验证登录
            # mobile = form.cleaned_data.get('mobile')
            # request.session['ID'] = mobile.id
            # request.session['mobile'] = mobile.mobile
            ################

            # 获取清洗后的数据
            cleaned = form.cleaned_data
            # 将密码进行加密
            # 取出清洗后的用户名
            mobile = cleaned.get('mobile')
            # 取出清洗后的密码
            password = cleaned.get('password')
            h = hashlib.md5(password.encode("utf-8"))  # 将传入的密码进行md5加密
            password = h.hexdigest()
            # print(name,password)
            # 从数据库查询
            try:
                Users.objects.get(mobile=mobile, password=password)
                # 跳转到登录页
                return redirect(request, "users/index.html")
            except:
                return render(request, "users/login.html")

        else:  # 不合法
            context = {
                'errors': form.errors,
            }
            return render(request, "users/login.html", context=context)
