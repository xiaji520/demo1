import random
import re
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from django_redis import get_redis_connection
from Supermarket.settings import SECRET_KEY
from db.base_view import VerifyLoginView
from users.forms import RegisterForm, LoginForm, InforForm, ForgetForm, PasswordForm
from users.models import Users
from users.helper import set_password, login, send_sms






class RegisterView(View):
    '''注册视图'''
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


class SendMsg(View):
    """
    发送短消验证码
    """

    def get(self, request):
        pass

    def post(self, request):
        # 1. 接收参数
        mobile = request.POST.get('mobile', '')
        rs = re.search('^1[3-9]\d{9}$', mobile)
        # 判断参数合法性
        if rs is None:
            return JsonResponse({'error': 1, 'errmsg': '电话号码格式错误!'})
        # 2. 处理数据
        # 先模拟,最后接入运营商
        """
            1. 生成随机验证码
            2. 保存验证码 保存到redis中, 存取速度快,并且可以方便的设置有效时间
            3. 接入运营商
        """
        # 1. 生成随机验证码字符串
        random_code = "".join([str(random.randint(0, 9)) for _ in range(6)])
        print("验证码为:{}".format(random_code))

        # 2. 保存验证码到redis中
        # 获取连接
        r = get_redis_connection()
        # 保存手机号码对应的验证码
        r.set(mobile, random_code)
        r.expire(mobile, 60)  # 设置60秒后过期

        # 获取当前手机号码的发送次数
        key_times = "{}_times".format(mobile)
        now_times = r.get(key_times)
        if now_times is None or int(now_times) < 5:  # 从redis获取的二进制,需要转换
            # 限制发送验证码次数, 不能超过5次
            r.incr(key_times)
            # 设置一个过期时间,一个小时
            r.expire(key_times, 3600)
        else:
            # 返回发送次数过多
            return JsonResponse({"error": 1, "errmsg": "发送次数过多,请一小时后再试!"})

        # # 3. 接入运营商
        __business_id = uuid.uuid1()
        params = "{\"code\":\"%s\",\"product\":\"xiaji blog\"}" % random_code
        # print(params)
        rs = send_sms(__business_id, mobile, "注册验证", "SMS_2245271", params)
        print(rs.decode('utf-8'))

        # 3. 合成响应
        return JsonResponse({'error': 0})


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
            # id
            # form.verify_password(request)
            ################  写在helper.py里面封装了
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
        # 显示账号信息
        # 通过id查询数据
        user_id = request.session.get('ID')
        # print(user_id)
        user = Users.objects.get(pk=user_id)
        # print(user)
        context = {
            'user': user
        }

        return render(request, "users/infor.html", context=context)

    def post(self, request):
        # 接收参数
        data = request.POST
        # 验证数据的合法性
        form = InforForm(data)
        if form.is_valid():
            # 获取id
            user_id = request.session.get('ID')

            # 获取清洗后的数据
            cleaned = form.cleaned_data
            # 取出清洗后信息
            nickname = cleaned.get('nickname')
            birthday = cleaned.get('birthday')
            school = cleaned.get('school')
            location = cleaned.get('location')
            hometown = cleaned.get('hometown')

            # 保存数据库
            Users.objects.filter(id=user_id).update(#nickname=nickname,
                                                    birthday=birthday,
                                                    school=school,
                                                    location=location,
                                                    hometown=hometown
                                                    )
            return redirect("users/login.html")

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

        # 通过id查询数据
        user_id = request.session.get('ID')
        # print(user_id)
        user = Users.objects.get(pk=user_id)
        if form.is_valid():
            # 获取清洗后的数据
            cleaned = form.cleaned_data
            # 取出清洗后的密码
            # 将密码进行加密
            password = set_password(cleaned.get('password'))
            # 修改到数据库
            # 验证原密码是否存在,不能用get,用filter
            if Users.objects.filter(user=user, password=password).exists():
                password2 = set_password(cleaned.get('password2'))
                # 验证原密码是否存在
                Users.objects.filter(password=password).update(password=password2)
                # 跳转到登录页
                return redirect('users:登录')
        else:
            # 错误
            return render(request, 'users/password.html', context={'errors': form.errors, })
