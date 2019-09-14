from django.shortcuts import render,redirect,HttpResponse
import datetime
from .models import *
from myapp.models import User
from django.urls import reverse
import os
from django.core.paginator import Paginator
from django.conf import settings
from django.utils import timezone
# Create your views here.


#发布文章
def test(request,id):
    if request.method == 'GET':
        print("11111111111")
        return render(request,'gxGO/fabu.html',{'id':id})
    else:
        if id == '000000':
            fb = article()
            fb.title = request.POST.get('title')
            fb.keyWord = request.POST.get('keywords')
            fb.summary = request.POST.get('summary')
            fb.content = request.POST.get('content')
            fb.createTime = timezone.now()
            try:
                h = request.session.get("user_token")
                user = User.objects.get(user_token = h)
                f = request.FILES.get('fileup')
                print("**************")
                if f:
                    print("**************")
                    filePath = os.path.join(settings.MDEIA_ROOT, f.name)
                    print(filePath)
                    with open(filePath, 'wb')as fp:
                        for info in f.chunks():
                            fp.write(info)
                    fb.mainimg = f.name
                fb.art_id = user
                fb.save()
                return redirect(reverse('myapp:mine',args=(1,)))
            except User.DoesNotExist as e:
                return HttpResponse("发布失败")
        else:
            try:
                ari = article.objects.get(pk = id)
                ari.title = request.POST.get('title')
                ari.keyWord = request.POST.get('keywords')
                ari.summary = request.POST.get('summary')
                ari.content = request.POST.get('content')
                img = request.FILES.get('fileup')
                if img:
                    filePath = os.path.join(settings.MDEIA_ROOT, img.name)
                    with open(filePath, 'wb')as fp:
                        for info in img.chunks():
                            fp.write(info)
                    ari.mainimg = img.name
                ari.save()
                return redirect(reverse('myapp:mine',args=(1,)))
            except Exception as e:
                return HttpResponse(e)


#文章页面
def show(request,num,page):
    fab = article.objects.get(pk = num)
    print(fab.PV,type(fab.PV))
    fab.PV = fab.PV+1
    fab.save()
    comlist = fab.comments.all()
    userId = fab.art_id
    username = userId.username

    print(username)
    print(fab)
    print("222222222222")
    paginator = Paginator(comlist, 10)
    pagenum = paginator.page(page)
    last = pagenum.number
    next = pagenum.number
    if pagenum.has_previous():
        last = pagenum.previous_page_number()
    if pagenum.has_next():
        next = pagenum.next_page_number()
    list = []
    try:
        isUser = False
        user_token = request.session.get('user_token')
        user = User.objects.get(user_token=user_token)
        if fab.art_id == user:
            isUser = True
    except Exception as e:
        print(e)
    for i in pagenum:
        try:
            print(i)

            user = User.objects.get(pk = i.writer_id)
            data = {
                'id':i.pk,
                'username': user.username,
                'body': i.body,
                'time': i.created
            }
            list.append(data)
        except Exception as e:
            print(e)
    writerAllari = userId.article_set.all()
    print(writerAllari)
    return render(request,'gxGO/show.html',{'fab':fab,
                                            'username':username,
                                            'writername':userId.username,
                                            'img': userId.img,
                                            'indiResume': userId.individualResume,
                                            'num':num,
                                            'page':page,
                                            'writerAllList':writerAllari,
                                            'comlist':list,
                                            'last':last,
                                            'next':next,
                                            'isUser':isUser})

def delete(request,id):
    user_token = request.session.get('user_token')
    try:
        ari = article.objects.get(pk = id)
        user = User.objects.get(user_token = user_token)
        if ari.art_id == user:
            ari.delete()
            return redirect(reverse('myapp:mine',args=(1,)))
        else:
            return HttpResponse('非法操作')
    except Exception as e:
        print('11111111')
        return HttpResponse(e)
    return HttpResponse(id)

