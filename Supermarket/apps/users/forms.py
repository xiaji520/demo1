from django import forms
from django.core import validators
from django.core.validators import RegexValidator
from django_redis import get_redis_connection

from users.helper import set_password
from users.models import Users, UserAddress


# 注册
class RegisterForm(forms.Form):
    mobile = forms.CharField(max_length=11,
                             error_messages={'required': '请填写手机号!'},
                             validators=[RegexValidator(r'^1[3-9]\d{9}$', message="手机号码格式错误!")]
                             )
    password = forms.CharField(max_length=20,
                               min_length=6,
                               error_messages={
                                   'required': '请填写密码!',
                                   'min_length': '请输入至少六个字符!',
                                   'max_length': '请输入小于或等于二十个字符!'
                               })
    repassword = forms.CharField(max_length=20,
                                 min_length=6,
                                 error_messages={
                                     'required': '这是必填选项!',
                                     'min_length': '请输入至少六个字符!',
                                     'max_length': '请输入小于或等于二十个字符!'
                                 })
    # 验证码
    captcha = forms.CharField(max_length=6,
                              error_messages={
                                  'required': "验证码必须填写!"
                              })

    agree = forms.BooleanField(error_messages={
        'required': '必须同意用户协议!'
    })

    def clean(self):
        pwd = self.cleaned_data.get("password")  # 密码
        repwd = self.cleaned_data.get("repassword")  # 重复密码
        if pwd and repwd and pwd != repwd:
            raise forms.ValidationError({"repassword": "两次密码不一致,请重新输入!"})

        # 验证 用户传入的验证码和redis中的是否一样
        # 用户传入
        try:
            captcha = self.cleaned_data.get('captcha')
            mobile = self.cleaned_data.get('mobile', '')
            # 获取redis中的
            r = get_redis_connection()
            random_code = r.get(mobile)  # 二进制, 转码
            random_code = random_code.decode('utf-8')
            # 比对
            if captcha and captcha != random_code:
                raise forms.ValidationError({"captcha": "验证码输入错误!"})
        except:
            raise forms.ValidationError({"captcha": "验证码输入错误!"})

        # 返回,返回整个清洗后的数据
        return self.cleaned_data

    def clean_mobile(self):  # 验证用户名是否重复
        mobile = self.cleaned_data.get('mobile')
        flag = Users.objects.filter(mobile=mobile).exists()
        if flag:
            # 存在 错误
            raise forms.ValidationError("该手机已注册,请直接登录!")
        else:
            return mobile


# 登录
class LoginForm(forms.Form):
    mobile = forms.CharField(max_length=11,
                             error_messages={
                                 'required': '请填写手机号!',
                                 'max_length': '请输入十一位电话号码!',
                             })
    password = forms.CharField(max_length=20,
                               min_length=6,
                               error_messages={
                                   'required': '请填写密码!',
                                   'min_length': '请输入至少六个字符!',
                                   'max_length': '请输入小于或等于二十个字符!'
                               })

    def clean(self):
        # 验证用户名
        mobile = self.cleaned_data.get('mobile')
        password = self.cleaned_data.get('password')
        # 验证手机号
        try:
            user = Users.objects.get(mobile=mobile)
        except Users.DoesNotExist:
            raise forms.ValidationError({'mobile': '用户名错误'})
        # 验证密码
        if user.password != set_password(password):
            raise forms.ValidationError({'password': '密码填写错误'})

        # ################
        # # 用于session验证登录
        self.cleaned_data['user'] = user
        # 返回,返回整个清洗后的数据
        return self.cleaned_data
        # ################


# 个人资料
class InforForm(forms.Form):
    nickname = forms.CharField(max_length=50,
                               min_length=2,
                               error_messages={
                                   'required': '请填写昵称!',
                                   'min_length': '请输入至少两个个字符!',
                                   'max_length': '请输入小于或等于五十个字符!'
                               })


# 忘记密码
class ForgetForm(forms.Form):
    mobile = forms.CharField(max_length=11,
                             error_messages={'required': '请填写手机号!'},
                             validators=[RegexValidator(r'^1[3-9]\d{9}$', message="手机号码格式错误!")]
                             )
    password2 = forms.CharField(max_length=20,
                                min_length=6,
                                error_messages={
                                    'required': '请填写密码!',
                                    'min_length': '请输入至少六个字符!',
                                    'max_length': '请输入小于或等于二十个字符!'
                                })
    repassword2 = forms.CharField(max_length=20,
                                  min_length=6,
                                  error_messages={
                                      'required': '这是必填选项!',
                                      'min_length': '请输入至少六个字符!',
                                      'max_length': '请输入小于或等于二十个字符!'
                                  })
    # 验证码
    captcha = forms.CharField(max_length=6,
                              error_messages={
                                  'required': "验证码必须填写!"
                              })

    def clean(self):
        pwd = self.cleaned_data.get("password")  # 密码
        repwd = self.cleaned_data.get("repassword")  # 重复密码
        if pwd and repwd and pwd != repwd:
            raise forms.ValidationError({"repassword": "两次密码不一致,请重新输入!"})
        # 返回,返回整个清洗后的数据
        return self.cleaned_data

    def clean_mobile(self):  # 验证用户名是否存在
        mobile = self.cleaned_data.get('mobile')
        flag = Users.objects.filter(mobile=mobile).exists()
        if flag:
            # 存在 正确
            return mobile
        else:
            raise forms.ValidationError("该手机未注册,请注册!")


# 修改密码
class PasswordForm(forms.Form):
    password = forms.CharField(max_length=20,
                               min_length=6,
                               error_messages={
                                   'required': '请填写密码!',
                                   'min_length': '请输入至少六个字符!',
                                   'max_length': '请输入小于或等于二十个字符!'
                               })
    password2 = forms.CharField(max_length=20,
                                min_length=6,
                                error_messages={
                                    'required': '请填写修改密码!',
                                    'min_length': '请输入至少六个字符!',
                                    'max_length': '请输入小于或等于二十个字符!'
                                })
    repassword2 = forms.CharField(max_length=20,
                                  min_length=6,
                                  error_messages={
                                      'required': '这是必填选项!',
                                      'min_length': '请输入至少六个字符!',
                                      'max_length': '请输入小于或等于二十个字符!'
                                  })

    def clean(self):
        pwd = self.cleaned_data.get("password2")  # 密码
        repwd = self.cleaned_data.get("repassword2")  # 重复密码
        if pwd and repwd and pwd != repwd:
            raise forms.ValidationError({"repassword2": "两次密码不一致,请重新输入!"})
        # 返回,返回整个清洗后的数据
        return self.cleaned_data


# 用户添加收货地址的表单
class AddressAddForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        exclude = ['create_time', 'update_time', 'is_delete', 'user']
        error_messages = {
            'username': {
                'required': "请填写用户名！",
            },
            'phone': {
                'required': "请填写手机号码！",
            },
            'brief': {
                'required': "请填写详细地址！",
            },
            'hcity': {
                'required': "请填写完整地址！",
            },
        }

    def clean(self):
        # 验证如果数据库里地址已经超过6六表报错
        cleaned_data = self.cleaned_data
        count = UserAddress.objects.filter(user_id=self.data.get("user_id")).count()
        if count >= 6:
            raise forms.ValidationError({"hcity": "收货地址最多只能保存6条"})

        # 默认地址操作
        if cleaned_data.get('isDefault'):
            UserAddress.objects.filter(user_id=self.data.get("user_id")).update(isDefault=False)
        return cleaned_data
