from django.db import models
from myapp.models import User
from django.contrib import admin
# Create your models here.
# 闪购左侧模型
class FoodType(models.Model):
    typeid = models.CharField(max_length=60)
    typename = models.CharField(max_length=100)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)
    class Meta:
        db_table = 'FoodType'


class Goods(models.Model):
    productid = models.CharField(max_length=16)  # 商品的id
    productimg = models.CharField(max_length=200)  # 商品的图片
    productname = models.CharField(max_length=100)  # 商品的名称
    productlongname = models.CharField(max_length=200)  # 商品的规格
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100)  # 规格
    price = models.FloatField(default=0)  # 商品的折后价格
    marketprice = models.FloatField(default=1)  # 商品的原价
    categoryid = models.CharField(max_length=16)  # 分类的id
    childcid = models.CharField(max_length=16)  # 子分类的id
    childcidname = models.CharField(max_length=100)  # 子分类的名称
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)  # 排序
    productnum = models.IntegerField(default=1)  # 销量排序
    class Meta:
        db_table = 'Goods'
        verbose_name = '货物'
        verbose_name_plural = '货物类'
    def __str__(self):
        return self.productlongname



class Order(models.Model):
    good = models.ForeignKey(Goods,on_delete=models.CASCADE,related_name='orders')
    buyer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    isSold = models.BooleanField(default=False)
    num = models.IntegerField(default=0)
    sum = models.CharField(max_length=20,default=0)
    createTime = models.DateTimeField(null=True)
    class Meta:
        db_table = 'orders'
        verbose_name = '订单'
        verbose_name_plural = '订单类'

    @classmethod
    def createOrder(cls, good, buyer,num,sum):
        u = cls(good=good, buyer=buyer,num = num,sum = sum)
        return u


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    def pk(self):
        return self.pk
    pk.short_description = '货物编号'
    def productid(self):
        return self.productid
    productid.short_description = '商品id'
    def productname(self):
        return self.productname
    productname.short_description = '商品名称'
    def productlongname(self):
        return self.productlongname
    productlongname.short_description = '商品规格'
    def productimg(self):
        return self.productimg
    productimg.short_description = '商品图片'
    def price(self):
        return self.price
    price.short_description = '商品价格'
    def marketprice(self):
        return self.marketprice
    marketprice.short_description = '商品原价'
    def productnum(self):
        return self.productnum
    productnum.short_description = '销量'
    list_display = [
        pk,
        productid,
        productname,
        productlongname,
        productimg,
        price,
        marketprice,
        productnum
    ]
    search_fields = ['productlongname']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    def pk(self):
        return self.pk
    pk.short_description = '订单编号'
    def good(self):
        return self.good
    good.short_description = '商品名'
    def buyer(self):
        return self.buyer
    buyer.short_description = '买家'
    def isSold(self):
        if self.isSold:
            return '已购买'
        else:
            return '未购买'
    isSold.short_description = '订单情况'
    def num(self):
        return self.num
    num.short_description = '商品数量'
    def sum(self):
        return self.sum
    sum.short_description = '交易金额'
    def createTime(self):
        return self.createTime
    createTime.short_description = '订单时间'
    list_display = [
        pk,
        good,
        buyer,
        isSold,
        num,
        sum,
        createTime,
    ]
    list_filter = ['buyer']
    search_fields = ['good']

#购物车
class Cart(models.Model):
    good = models.ForeignKey(Goods,on_delete=models.CASCADE,related_name='carts')
    buyer = models.ForeignKey(User,on_delete=models.CASCADE,related_name='carts')
    isSold = models.BooleanField(default=False)
    num = models.IntegerField(default=1)
    sum = models.CharField(max_length=20,default=0)
    createTime = models.DateTimeField(null=True)
    class Meta:
        db_table = 'carts'
        verbose_name = '购物车'
        verbose_name_plural = '购物车类'
    @classmethod
    def createCart(cls, good, buyer):
        u = cls(good=good, buyer=buyer)
        return u
@admin.register(Cart)
class cartAdmin(admin.ModelAdmin):
    def pk(self):
        return self.pk
    pk.short_description = '购物车编号'
    def good(self):
        return self.good
    good.short_description = '商品名'
    def buyer(self):
        return self.buyer
    buyer.short_description = '买家'
    def isSold(self):
        if self.isSold:
            return '已支付'
        else:
            return '未支付'
    isSold.short_description = '订单情况'
    def num(self):
        return self.num
    num.short_description = '商品数量'
    def sum(self):
        return self.sum
    sum.short_description = '交易金额'
    def createTime(self):
        return self.createTime
    createTime.short_description = '购物车订单时间'
    list_display = [
        pk,
        good,
        buyer,
        isSold,
        num,
        sum,
        createTime,
    ]
    list_filter = ['buyer']
    search_fields = ['good']
