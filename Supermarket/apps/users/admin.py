from django.contrib import admin

# Register your models here.
from users.models import Users


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    # 分页
    list_per_page = 5
    # 指定显示的列
    list_display = ['id',
                    'mobile',
                    'password',
                    'nickname',
                    'sex',
                    'birthday',
                    'school',
                    'location',
                    'hometown',
                    'head',
                    'is_delete',
                    'create_time',
                    'update_time']
    # 设置可编辑连接字段
    list_display_links = ['id', 'mobile', 'password', 'nickname', ]
