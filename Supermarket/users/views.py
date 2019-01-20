import hashlib

from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from users.forms import RegisterForm, LoginForm
from users.models import Users


def register(request):  # 注册 ^register$
    if request.method == "POST":
        # 接收参数
        data = request.POST
        # 验证数据合法性
        form = RegisterForm(data)  # 实例化form对象
        if form.is_valid():  # 合法
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
        else:  # 不合法
            context = {
                'errors': form.errors,
            }
            return render(request, "users/reg.html", context=context)
    else:
        return render(request, "users/reg.html")


def login(request):  # 登录 ^login$
    if request.method == "POST":
        # 接收参数
        data = request.POST
        # 验证数据合法性
        form = LoginForm(data)  # 实例化form对象
        if form.is_valid():  # 合法

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
                return HttpResponse('ok!')
            except:
                return render(request, "users/login.html")

        else:  # 不合法
            context = {
                'errors': form.errors,
            }
            return render(request, "users/login.html", context=context)
    else:
        return render(request, "users/login.html")
