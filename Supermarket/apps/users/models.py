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
