import hashlib

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from Supermarket.settings import SECRET_KEY
from db.base_view import VerifyLoginView
from users.forms import RegisterForm, LoginForm, InforForm, ForgetForm, PasswordForm
from users.models import Users
from users.helper import set_password, login


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
            password = set_password(cleaned.get('password'))
            # print(password)
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
            ################写在helper.py里面封装了
            # session验证登录
            # user = form.cleaned_data.get('user')
            # request.session['ID'] = user.id
            # request.session['mobile'] = user.mobile
            # request.session.set_expiry(0)
            # ///////////////////
            user = form.cleaned_data.get('user')
            login(request, user)
            ################

            # 获取清洗后的数据
            cleaned = form.cleaned_data
            # 将密码进行加密
            # 取出清洗后的手机号
            mobile = cleaned.get('mobile')
            # 取出清洗后的密码
            password = set_password(cleaned.get('password'))
            # 从数据库查询
            try:
                Users.objects.get(mobile=mobile, password=password)
                # 跳转到登录页
                return redirect('users:个人资料')
            except:
                return render(request, "users/login.html")
        else:  # 不合法
            context = {
                'errors': form.errors,
            }
            return render(request, "users/login.html", context=context)


class InforView(VerifyLoginView):  # 继承了VerifyLoginView,替换View,使登录session才能看到
    '''
    个人资料
    '''

    def get(self, request):
        return render(request, "users/infor.html")

    def post(self, request):
        # 接收参数
        data = request.POST
        # 验证数据的合法性
        form = InforForm(data)
        if form.is_valid():
            # 获取清洗后的数据
            cleaned = form.cleaned_data
            # 取出清洗后信息
            for _ in range(2000):
                pwd = cleaned.get('password')
                pass_str = "{}{}".format(pwd, SECRET_KEY)
                h = hashlib.md5(pass_str.encode("utf-8"))  # 将传入的密码进行md5加密(加密2000次,并且加盐)
                password = h.hexdigest()
                password = cleaned.get('password')
            mobile = cleaned.get('mobile')
            nickname = cleaned.get('nickname')
            sex = cleaned.get('sex')
            birthday = cleaned.get('birthday')
            school = cleaned.get('school')
            location = cleaned.get('location')
            hometown = cleaned.get('hometown')
            mobile2 = cleaned.get('mobile2')

            # 保存数据库
            Users.objects.filter(mobile=mobile, password=password).update(nickname=nickname,
                                                                          sex=sex,
                                                                          birthday=birthday,
                                                                          school=school,
                                                                          location=location,
                                                                          hometown=hometown,
                                                                          )
            # return render(request, "users/infor.html")
            return HttpResponse('1111')

        else:  # 不合法
            context = {
                'errors': form.errors,
            }
            return render(request, "users/infor.html", context=context)


class ForgetView(VerifyLoginView):  # 继承了VerifyLoginView,替换View,使登录session才能看到
    """忘记密码"""

    def get(self, request):
        return render(request, 'users/forgetpassword.html')

    def post(self, request):
        # 接收参数
        data = request.POST

        # 验证数据的合法性
        form = ForgetForm(data)
        if form.is_valid():
            # 获取清洗后的数据
            cleaned = form.cleaned_data
            # 将密码进行加密
            # 取出清洗后的手机号
            mobile = cleaned.get('mobile')
            # 取出清洗后的密码
            password = set_password(cleaned.get('password'))
            # 修改到数据库
            # 验证原密码是否存在,不能用get,用filter
            if Users.objects.filter(mobile=mobile, password=password).exists():
                return render(request, 'users/forgetpassword.html')

            Users.objects.filter(mobile=mobile).update(password=password)
            # 跳转到登录页
            return redirect('users:登录')
        else:
            # 错误
            return render(request, 'users/forgetpassword.html', context={'errors': form.errors, })


class PasswordView(VerifyLoginView):  # 继承了VerifyLoginView,替换View,使登录session才能看到
    """修改密码"""

    def get(self, request):
        return render(request, 'users/password.html')

    def post(self, request):
        # 接收参数
        data = request.POST

        # 验证数据的合法性
        form = PasswordForm(data)
        if form.is_valid():
            # 获取清洗后的数据
            cleaned = form.cleaned_data
            # 取出清洗后的密码
            # 将密码进行加密
            password = set_password(cleaned.get('password'))
            # 修改到数据库
            # 验证原密码是否存在,不能用get,用filter
            if Users.objects.filter(password=password).exists():
                password2 = set_password(cleaned.get('password2'))
                # 验证原密码是否存在
                Users.objects.filter(password=password).update(password=password2)
                # 跳转到登录页
                return redirect('users:登录')
        else:
            # 错误
            return render(request, 'users/password.html', context={'errors': form.errors, })
