import hashlib

from django.shortcuts import redirect

from Supermarket.settings import SECRET_KEY


# 密码加盐
def set_password(password):
    for _ in range(2000):
        # 循环加密 + 加盐
        pass_str = "{}{}".format(password, SECRET_KEY)
        h = hashlib.md5(pass_str.encode("utf-8"))  # 将传入的密码进行md5加密(加密2000次,并且加盐)
        password = h.hexdigest()

    # 返回密码
    return password


# 保存session的方法
def login(request, user):
    request.session['ID'] = user.id
    request.session['mobile'] = user.mobile
    request.session.set_expiry(0)


# 登录验证装饰器
def check_login(func):
    # 新函数
    def verify_login(request, *args, **kwargs):
        # 验证session中是否有登录标识
        if request.session.get("ID") is None:
            # 跳转到登录
            return redirect('users:登录')
        else:
            # 调用原函数
            return func(request, *args, **kwargs)

    # 返回新函数
    return verify_login
