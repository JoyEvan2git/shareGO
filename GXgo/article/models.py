from django.db import models
from myapp.models import User
from django.contrib import admin
from tinymce.models import HTMLField
# Create your models here.

class article(models.Model):
    title = models.CharField(max_length=100,null=True)
    content = HTMLField()
    summary = models.CharField(max_length=200,null=True)
    keyWord = models.TextField(max_length=200,null=True)
    mainimg = models.CharField(max_length=100,null=True)
    createTime = models.DateTimeField(null=True)
    art_id = models.ForeignKey(User,on_delete=models.CASCADE)
    isDelete = models.BooleanField(default=False)
    PV = models.IntegerField(default=0)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['pk']
        verbose_name = '文章'
        verbose_name_plural = '文章类'


@admin.register(article)
class articleAdmin(admin.ModelAdmin):
    def pk(self):
        return self.pk
    pk.short_description = '文章编号'
    def title(self):
        return self.title
    title.short_description = '标题'
    def content(self):
        return self.content[0:50]+'...'
    content.short_description = '内容'
    def summary(self):
        return self.summary
    summary.short_description = '简介'
    def keyWord(self):
        return self.keyWord
    keyWord.short_description = '关键字'
    def createTime(self):
        return self.createTime
    createTime.short_description = '创建时间'
    def art_id(self):
        return self.art_id
    art_id.short_description = '作者'

    def isDelete(self):
        if self.isDelete:
            return '未过审'
        else:
            return '已过审'
    isDelete.short_description = '过审情况'
    list_display = [
        pk, title,  content, summary, keyWord, createTime, art_id,isDelete
    ]
    search_fields = ['title']
