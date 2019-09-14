from django.db import models
from django.contrib import admin
# Create your models here.
#用户类
class User(models.Model):
    userAccount = models.CharField(max_length=20,unique=True)#用户账号
    individualResume = models.CharField(max_length=200,default='这个人很害羞，没有留点信息')#个人简介
    username = models.CharField(max_length=20)#用户名
    password = models.CharField(max_length=16)#密码
    address = models.CharField(max_length=50)#地址
    gender = models.BooleanField(default=True)#性别
    phone = models.CharField(max_length=11)#手机
    img = models.CharField(max_length=200,default='default.png')
    user_token = models.CharField(max_length=50,null = True)
    age = models.IntegerField(default=0)#年龄
    isDelete = models.BooleanField(default=False)#逻辑删除

    @classmethod
    def createUser(cls, userAccount, username, password):
        u = cls(userAccount = userAccount,username = username,password = password)
        return u
    def __str__(self):
        return self.username
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户类'
@admin.register(User)
class GradesAdmin(admin.ModelAdmin):
    def gender(self):
        if self.gender:
            return '男'
        else:
            return '女'
    gender.short_description = '性别'

    def pk(self):
        return self.pk
    pk.short_description = '编号'

    def username(self):
        return self.username
    username.short_description = '用户名'

    def userAccount(self):
        return self.userAccount
    userAccount.short_description = '账户'

    def password(self):
        return self.password
    password.short_description = '密码'

    def address(self):
        return self.address
    address.short_description = '地址'

    def phone(self):
        return self.phone
    phone.short_description = '联系电话'

    def age(self):
        return self.age
    age.short_description = '年龄'

    def isDelete(self):
        if self.isDelete:
            return '账户已注销'
        else:
            return '账户正常'
    isDelete.short_description = '逻辑删除'

    list_display = [
        pk,username,userAccount,password,address,gender,phone,age,isDelete
    ]
    search_fields = ['username']
