from django import forms
from users.models import Users


# 注册
class RegisterForm(forms.Form):
    mobile = forms.CharField(max_length=14,
                             min_length=11,
                             error_messages={
                                 'required': '请填写手机号!',
                                 'min_length': '请输入至少十一个字符!',
                                 'max_length': '请输入小于或等于十四个字符!'
                             })
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

    def clean(self):
        pwd = self.cleaned_data.get("password")  # 密码
        repwd = self.cleaned_data.get("repassword")  # 重复密码
        if pwd and repwd and pwd != repwd:
            raise forms.ValidationError({"repassword": "两次密码不一致,请重新输入!"})
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
    mobile = forms.CharField(max_length=14,
                             min_length=11,
                             error_messages={
                                 'required': '请填写手机号!',
                                 'min_length': '请输入至少十一个字符!',
                                 'max_length': '请输入小于或等于十四个字符!'
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
        # 查询数据库
        try:
            mobile = Users.objects.get(mobile=mobile)
        except Users.DoesNotExist:
            raise forms.ValidationError({'mobile': '用户名或者密码错误'})

        # ################
        # # 用于session验证登录
        # self.cleaned_data['mobile'] = mobile
        # ################

        # 返回,返回整个清洗后的数据
        # return self.cleaned_data
