from django.db import models
from article.models import article
from myapp.models import User
from django.contrib import admin
# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(
        article,
        on_delete=models.CASCADE,
        related_name= 'comments'
    )
    writer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)
        verbose_name = '评论'
        verbose_name_plural = '评论类'

    def __str__(self):
        return self.body[:20]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    def pk(self):
        return self.pk
    pk.short_description = '编号'
    def writer(self):
        return self.writer
    writer.short_description = '评论者'
    def body(self):
        return self.body
    body.short_description = '内容'
    def created(self):
        return self.created
    created.short_description = '评论时间'
    def post(self):
        return self.post
    pk.short_description = '评论帖子'
    list_display = [
        pk, writer,  body, created, post
    ]
    search_fields = ['body']
