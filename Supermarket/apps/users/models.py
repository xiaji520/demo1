

from django.db import models


# Create your models here.
class Users(models.Model):
    mobile = models.CharField(max_length=14)  # 手机号
    password = models.CharField(max_length=32)  # 密码
    name = models.CharField(max_length=20, null=True)  # 昵称
    sex_choices = (
        (1, '男'),
        (2, '女'),
    )
    sex = models.SmallIntegerField(choices=sex_choices, default=2)  # 性别
    birthday = models.DateTimeField(null=True)  # 生日
    school = models.CharField(max_length=100, null=True)  # 学校
    location = models.CharField(max_length=100, null=True)  # 地址
    hometown = models.CharField(max_length=100, null=True)  # 家庭地址
    is_delete = models.BooleanField(default=False)  # 是否删除
    add_time = models.DateTimeField(auto_now_add=True)  # 添加时间
    update_time = models.DateTimeField(auto_now=True)  # 更新时间

    class Meta:
        db_table = "users"  # 表名
