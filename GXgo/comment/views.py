from django.shortcuts import render,HttpResponse,redirect
from .models import Comment
from django.urls import reverse
from article.models import article
from myapp.models import User
import datetime
# Create your views here.


def postCom(request,id,page):
    if request.method == 'POST':
        print("11111")
        text = request.POST.get('text')
        user_token = request.session.get('user_token')
        try:
            com = Comment()
            user = User.objects.get(user_token=user_token)

            print("22222")
            ari = article.objects.get(pk=id)

            print("22222")
            com.body = text
            print("22222")
            com.created = datetime.datetime.now()
            print("22222")
            com.writer = user
            print("22222")
            com.post = ari
            print("22222")
            com.save()
            print("22222")
            print(type(id),id)
            return redirect(reverse('article:show',args=(id,page)))
        except Exception as e:
            print(e)
            return HttpResponse('评论失败')
    else:
        print("4444")
        return HttpResponse('评论失败')

def delete(request,id):
    try:
        com = Comment.objects.get(pk = id)
        a = com.post_id
        ari = article.objects.get(pk = a)
        user = ari.art_id
        print(user)
        user_token = request.session.get('user_token')
        u = User.objects.get(user_token=user_token)
        if user == u:
            com.delete()
            return redirect(reverse('article:show',args=(a,1)))
    except Exception as e:
        return redirect(reverse('myapp:index'))
    return HttpResponse('非法操作')