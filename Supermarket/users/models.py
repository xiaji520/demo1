from django.db import models


# Create your models here.
class Users(models.Model):
    mobile = models.CharField(max_length=14)  # 手机号
    password = models.CharField(max_length=32)  # 密码

    class Meta:
        db_table = "users"  # 表名
