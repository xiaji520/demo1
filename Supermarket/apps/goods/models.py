from django.db import models
from db.base_model import BaseModel

is_on_sale_choices = (
    (False, "下架"),
    (True, "上架"),
)


# 商品模型一：
# 商品分类
# ID
# 分类名称
# 描述
# 排序
class Category(BaseModel):
    cate_name = models.CharField(verbose_name='分类名称',
                                 max_length=20
                                 )
    brief = models.CharField(verbose_name='描述',
                             max_length=200,
                             null=True,
                             blank=True
                             )
    order = models.SmallIntegerField(default=0, verbose_name="排序")

    def __str__(self):
        return self.cate_name

    class Meta:
        verbose_name = "商品分类管理"
        verbose_name_plural = verbose_name


# 商品模型二:
# 商品SKU单位
# ID
# 单位（斤，箱）
class Unit(BaseModel):
    name = models.CharField(max_length=20,
                            verbose_name="单位")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "商品单位管理"
        verbose_name_plural = verbose_name


# 商品模型三：
# 商品SPU表
# ID
# 商品SPU名称
# 商品详情
class GoodsSPU(BaseModel):
    spu_name = models.CharField(verbose_name='商品SPU名称',
                                max_length=20
                                )
    content = models.TextField(verbose_name="商品详情")

    def __str__(self):
        return self.spu_name

    class Meta:
        verbose_name = "商品SPU"
        verbose_name_plural = verbose_name


# 模型四：
# 商品SKU表
# ID
# 商品SKU名称
# 商品的简介
# 价格
# 单位
# 库存
# 销量
# 封面图片
# 是否上架
# 商品分类
# 商品SPU
class GoodsSKU(BaseModel):
    sku_name = models.CharField(verbose_name='商品SKU名称',
                                max_length=100,
                                )
    brief = models.CharField(verbose_name="商品的简介",
                             max_length=200,
                             null=True,
                             blank=True,
                             )
    price = models.DecimalField(verbose_name='价格',
                                max_digits=9,
                                decimal_places=2,
                                default=0,
                                )
    unit = models.ForeignKey(to="Unit", verbose_name="单位")

    stock = models.IntegerField(verbose_name='库存',
                                default=0)

    sale_num = models.IntegerField(verbose_name='销量',
                                   default=0)

    # 默认相册中的第一张图片作为封面图片
    logo = models.ImageField(verbose_name='封面图片',
                             upload_to='goods/%Y%m/%d'
                             )

    is_on_sale = models.BooleanField(verbose_name="是否上架",
                                     choices=is_on_sale_choices,
                                     default=False)

    category = models.ForeignKey(to="Category",
                                 verbose_name='商品分类'
                                 )

    goods_spu = models.ForeignKey(to="GoodsSPU", verbose_name="商品SPU")

    def __str__(self):
        return self.sku_name

    class Meta:
        verbose_name = "商品SKU管理"
        verbose_name_plural = verbose_name


# 模型五：
# 商品相册管理
# ID
# 商品相册
# 相册图片地址
# 商品SKU
class Gallery(BaseModel):
    img_url = models.ImageField(verbose_name='相册图片地址',
                                upload_to='goods_gallery/%Y%m/%d'
                                )

    goods_sku = models.ForeignKey(to="GoodsSKU", verbose_name="商品SKU")

    class Meta:
        verbose_name = "商品相册管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "商品相册:{}".format(self.img_url.name)

# 模型六：
# 首页轮播
# ID
# 轮播活动名
# 轮播图片地址
# 排序
# 商品SKU
class Banner(BaseModel):
    name = models.CharField(verbose_name="轮播活动名",
                            max_length=150,
                            )
    img_url = models.ImageField(verbose_name='轮播图片地址',
                                upload_to='banner/%Y%m/%d'
                                )
    order = models.SmallIntegerField(verbose_name="排序",
                                     default=0,
                                     )

    goods_sku = models.ForeignKey(to="GoodsSKU", verbose_name="商品SKU")

    class Meta:
        verbose_name = "轮播管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

# 模型七：
# 首页活动
# ID
# 活动名称
# 活动图片地址
# 活动的url地址
class Activity(BaseModel):
    title = models.CharField(verbose_name='活动名称', max_length=150)
    img_url = models.ImageField(verbose_name='活动图片地址',
                                upload_to='activity/%Y%m/%d'
                                )
    url_site = models.URLField(verbose_name='活动的url地址', max_length=200)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "活动管理"
        verbose_name_plural = verbose_name

# 模型八：
# 首页活动专区
# ID
# 活动专区名称
# 排序
# 上否上线
# 商品
class ActivityZone(BaseModel):
    title = models.CharField(verbose_name='活动专区名称', max_length=150)
    brief = models.CharField(verbose_name="活动专区的简介",
                             max_length=200,
                             null=True,
                             blank=True,
                             )
    order = models.SmallIntegerField(verbose_name="排序",
                                     default=0,
                                     )
    is_on_sale = models.BooleanField(verbose_name="上否上线",
                                     choices=is_on_sale_choices,
                                     default=0,
                                     )
    goods_sku = models.ManyToManyField(to="GoodsSKU", verbose_name="商品")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "活动专区管理"
        verbose_name_plural = verbose_name
