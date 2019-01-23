from django.contrib import admin

# Register your models here.
from goods.models import Category, Unit, GoodsSPU, Gallery, GoodsSKU, Banner, Activity, ActivityZone


# 1.商品分类管理
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # 分页
    list_per_page = 5
    # 指定显示的列
    list_display = ['id', 'cate_name', 'brief', 'order', 'update_time']
    # 设置可编辑连接字段
    list_display_links = ['id', 'cate_name', 'brief']


# 2.商品单位管理
admin.site.register(Unit)
# 3.商品SPU
admin.site.register(GoodsSPU)


# 4.商品SKU管理
class GalleryInline(admin.TabularInline):  # 关联模型
    model = Gallery
    extra = 2


@admin.register(GoodsSKU)
class GoodsSkuAdmin(admin.ModelAdmin):
    # 分页
    list_per_page = 5
    # 指定显示的列
    list_display = ["id", 'sku_name', 'price', 'unit', 'stock', 'sale_num', 'is_on_sale', 'category']
    # 设置可编辑连接字段
    list_display_links = ["id", 'sku_name', 'price']
    # 搜索框
    search_fields = ['sku_name', 'price', 'sale_num']
    inlines = [
        GalleryInline,
    ]


# 5.轮播管理
admin.site.register(Banner)
# 6.活动管理
admin.site.register(Activity)


# 7.活动专区管理
@admin.register(ActivityZone)
class ActivityZoneAdmin(admin.ModelAdmin):
    # 分页
    list_per_page = 5
    # 搜索框
    search_fields = ["id", 'title', 'brief', 'order', 'is_on_sale', 'goods_sku']
