from django.shortcuts import render,redirect,HttpResponse
# Create your views here.
from django.core.paginator import Paginator
from .models import User
from article.models import article
from market.models import Order
from myapp.models import User
from django.urls import reverse
from django.http import JsonResponse
from django.conf import settings
import random


#主页
def index(request):
    articleList = article.objects.filter(isDelete = 0).order_by('PV')
    return render(request,'gxGO/index.html',{'articleList':articleList})

#验证账户是否存在
def checkacc(request):
    acc = request.POST.get('acc')
    user = User.objects.filter(userAccount = acc)
    ret = {'msg': 0}
    if user.count() == 0:
        ret = {'msg': 1}
    return JsonResponse(ret)

#注册
def regist(request):
    account = request.POST.get("userAccount")
    psw = request.POST.get("psw")
    name = request.POST.get("userName")
    u = User.createUser(account,name,psw)
    u.user_token = '#'
    u.save()
    return redirect(reverse('myapp:index'))

#跳转到个人主页
def mine(request,pageid):
    print("1111111111111111")
    user_token = request.session.get('user_token')
    try:
        h = User.objects.get(user_token=user_token)
        ariticleList = article.objects.filter(art_id=h)
        paginator = Paginator(ariticleList,4)
        print(type(pageid))
        page = paginator.page(pageid)
        last = pageid
        next = pageid
        if page.has_previous():
            last = page.previous_page_number()
        if page.has_next():
            next = page.next_page_number()

        return render(request, 'gxGO/mine.html', {'ariticleList': page,
                                                  'user':h,
                                                  'nextpage':next,
                                                  'lastpage':last})
    except Exception as e:
        print(e)
        return redirect('myapp:index')
    return HttpResponse('跳转失败')




#验证码
def verifycode(request):
    from PIL import Image,ImageDraw,ImageFont

    import random

    bgcolor = (random.randrange(20,100),
               random.randrange(20,100),
               random.randrange(20,100))
    width = 100
    height = 50

    im = Image.new('RGB',(width,height),bgcolor)

    draw = ImageDraw.Draw(im)

    for i in range(0,100):
        xy = (random.randrange(0,width),random.randrange(0,height))
        fill = (random.randrange(0,255),255,random.randrange(0,255))
        draw.point(xy,fill = fill)

    str = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    rand_str = ''
    for i in range(0,4):
        rand_str += str[random.randrange(0,len(str))]

    font = ImageFont.truetype(r"C:\Windows\Fonts\Arial.ttf",40)

    fontcolor1 = (255,random.randrange(0,255),random.randrange(0,255))
    fontcolor2 = (255,random.randrange(0,255),random.randrange(0,255))
    fontcolor3 = (255,random.randrange(0,255),random.randrange(0,255))
    fontcolor4 = (255,random.randrange(0,255),random.randrange(0,255))

    draw.text((5,2),rand_str[0],font = font,fill = fontcolor1)
    draw.text((25,2),rand_str[1],font = font,fill = fontcolor2)
    draw.text((50,2),rand_str[2],font = font,fill = fontcolor3)
    draw.text((75,2),rand_str[3],font = font,fill = fontcolor4)

    del draw

    request.session['verify'] = rand_str

    import io

    buf = io.BytesIO()

    im.save(buf,'png')
    return HttpResponse(buf.getvalue())

#登陆
def login(request):
    yzm = request.POST.get('yzm').upper()
    rand_str = request.session.get('verify').upper()
    ret = {'status': 0}
    if rand_str == yzm:
        ret['status'] = 1
        account = request.POST.get('account')
        psw = request.POST.get('psw')
        print(account, psw)
        try:
            h = User.objects.get(userAccount=account)
            if h.password == psw:
                ret['status'] = 2
                token = ''.join(random.sample('zyxwvutsrqponmlkjihgfedcba0123456789', 10))
                h.user_token = token
                h.save()
                request.session['user_token'] = h.user_token
                print(type(ret))
                return JsonResponse(ret)
        except Exception as e:
            print(e)
            print(type(ret))
        return JsonResponse(ret)
    print(type(ret))
    return JsonResponse(ret)


#注销
from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect(reverse('myapp:index'))

#修改信息
import os
def change(request,id,arid):
    if id == '1':
        user_token = request.session.get('user_token')
        try:
            h = User.objects.get(user_token=user_token)
        except Exception as e:
            return HttpResponse('修改失败')
        if request.method == 'GET':
            data = {
                'username':h.username,
                'address':h.address,
                'img':h.img,
                'phone':h.phone,
                'individualResume':h.individualResume
            }
            print(type(data))
            return render(request,'gxGO/change.html',{'h':data})
        elif request.method == 'POST':
            h.username = request.POST.get('username')
            h.gender = request.POST.get('sex')
            h.address = request.POST.get('address')
            h.age = int(request.POST.get('age'))
            h.phone = request.POST.get('phone')
            h.individualResume = request.POST.get('content')
            img = request.FILES.get('file')
            print(img)
            if img:
                filePath = os.path.join(settings.IMG_ROOT, img.name)
                print(filePath)
                with open(filePath, 'wb')as fp:
                    for info in img.chunks():
                        fp.write(info)
                imgName = img.name
                h.img = imgName
            h.save()
            return redirect('/home/change/1/0')
    elif id == '2':
        user_token = request.session.get('user_token')
        try:
            h = User.objects.get(user_token=user_token)
            ari = article.objects.get(pk=arid)
            print(ari.art_id,h)
            if h == ari.art_id:
                data = {
                    'title':ari.title,
                    'content':ari.content,
                    'summary':ari.summary,
                    'key':ari.keyWord,
                    'img':ari.mainimg
                }
                return render(request,'gxGO/fabu.html',{'data':data,
                                                        'id':ari.pk})
            else:
                return HttpResponse('错误访问')
        except Exception as e:
            print(e)
            return HttpResponse('404NOT FOUND嗷')


def isLogin(request):
    ret = {"status": 0}
    print(ret)
    try:
        user_token = request.session.get('user_token')
        if user_token:
            ret['status'] = 1
        return JsonResponse(ret)
    except Exception as e:
        return JsonResponse(ret)


#历史订单
def myorder(request,pageid):
    print(2222222)
    user_token = request.session.get('user_token')
    try:
        h = User.objects.get(user_token=user_token)
        myorder = h.orders.all().order_by('-createTime')
        paginator = Paginator(myorder, 8)
        page = paginator.page(pageid)
        last = page.number
        next = page.number
        if page.has_previous():
            last = page.previous_page_number()
        if page.has_next():
            next = page.next_page_number()
        return render(request, 'gxGO/myorder.html', {'orders': page,
                                                  'user': h,
                                                  'page':page.number,
                                                  'allpage':paginator.num_pages,
                                                  'nextpage': next,
                                                  'lastpage': last
                                                  })
    except Exception as e:
        print(e)
        return redirect('myapp:index')
    return HttpResponse('跳转失败')