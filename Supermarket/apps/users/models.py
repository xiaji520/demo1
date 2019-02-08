from django.core.validators import RegexValidator
from django.db import models

# Create your models here.
from db.base_model import BaseModel


class Users(BaseModel):  # BaseModel
    mobile = models.CharField(max_length=11,
                              verbose_name="手机号码",
                              )  # 手机号

    password = models.CharField(max_length=32,
                                verbose_name="密码"
                                )  # 密码

    nickname = models.CharField(max_length=50,
                                null=True,
                                blank=True,
                                verbose_name="昵称"
                                )  # 昵称

    sex_choices = (
        (1, '男'),
        (2, '女'),
    )
    sex = models.SmallIntegerField(choices=sex_choices,
                                   default=1,
                                   verbose_name="性别"
                                   )  # 性别

    birthday = models.DateField(null=True,
                                blank=True,
                                verbose_name="出生日期"
                                )  # 生日

    school = models.CharField(max_length=50,
                              null=True,
                              blank=True,
                              verbose_name="学校"
                              )  # 学校

    location = models.CharField(max_length=50,
                                null=True,
                                blank=True,
                                verbose_name="地址"
                                )  # 地址

    hometown = models.CharField(max_length=50,
                                null=True,
                                blank=True,
                                verbose_name="家乡"
                                )  # 家乡地址
    # 设置头像字段
    head = models.ImageField(upload_to="head/%Y%m", default="head/memtx.png", verbose_name="用户头像")

    def __str__(self):
        return self.mobile

    class Meta:
        db_table = "users"  # 表名
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name


class UserAddress(BaseModel):
    """用户收货地址管理"""
    user = models.ForeignKey(to="Users", verbose_name="创建人")
    username = models.CharField(verbose_name="收货人", max_length=100)
    phone = models.CharField(verbose_name="收货人电话",
                             max_length=11,
                             validators=[
                                 RegexValidator('^1[3-9]\d{9}$', '电话号码格式错误!')
                             ])
    hcity = models.CharField(verbose_name="省", max_length=100)
    hproper = models.CharField(verbose_name="市", max_length=100, blank=True, default='')
    harea = models.CharField(verbose_name="区", max_length=100, blank=True, default='')
    brief = models.CharField(verbose_name="详细地址", max_length=255)
    isDefault = models.BooleanField(verbose_name="是否设置为默认", default=False, blank=True)

    class Meta:
        verbose_name = "收货地址管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Payment(BaseModel):
    """
        支付方式
    """
    pay_name = models.CharField(verbose_name='支付方式',
                                max_length=20
                                )

    class Meta:
        verbose_name = "支付方式"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pay_name


class Transport(BaseModel):
    """
        配送方式
    """
    name = models.CharField(verbose_name='配送方式',
                            max_length=20
                            )
    money = models.DecimalField(verbose_name='金额',
                                max_digits=9,
                                decimal_places=2,
                                default=0
                                )

    class Meta:
        verbose_name = "配送方式"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
