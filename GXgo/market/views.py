from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
import json
from .models import FoodType,Goods,Order,Cart
from myapp.models import User
from django.core.paginator import Paginator
# Create your views here.
from article.models import article
from django.urls import reverse
from django.utils import timezone

#超市页面
def shop(request,categoryid,childcId,order_id,pageid):
    request.session['CAID'] = categoryid
    request.session['CID'] = childcId
    request.session['OID'] = order_id
    leftSlider = FoodType.objects.order_by('typesort')
    productList = Goods.objects.filter(categoryid=categoryid)
    if childcId != '0':
        productList = productList.filter(childcid=childcId)
    if order_id == '1':
        productList = productList.order_by("storenums")
    elif order_id == '2':
        productList = productList.order_by("-productnum")
    elif order_id == '3':
        productList = productList.order_by("price")
    elif order_id == '4':
        productList = productList.order_by("-price")
    childList = []
    group = leftSlider.get(typeid=categoryid)
    childnames = group.childtypenames.split('#')
    for str in childnames:
        arr = str.split(':')
        obj = {'childName': arr[0], 'childId': arr[1], 'categoryid': categoryid}
        childList.append(obj)
    paginator = Paginator(productList, 16)
    maxpage = paginator.num_pages
    pagenum = paginator.page(pageid)
    last = pagenum.number
    next = pagenum.number
    if pagenum.has_previous():
        last = pagenum.previous_page_number()
    if pagenum.has_next():
        next = pagenum.next_page_number()
    ari = article.objects.all().order_by('-PV')
    arilist = ari[0:6]
    return render(request, 'gxGO/market.html', {'title': "超市",
                                               'leftSlider': leftSlider,
                                                'arilist':arilist,
                                               'productList': pagenum,
                                               'childList': childList,
                                               'childcId': childcId,
                                               "order_id": order_id,
                                               'page':pageid,
                                               'maxpage':maxpage,
                                               'categoryid': categoryid,
                                               'last': last,
                                               'next': next,})

#加入购物车AJAX请求
def cart_ajax(request):
    h = request.session.get('user_token')
    ret = {"status": 0}
    if h:
        goodid = request.POST.get("goodNum")
        good = Goods.objects.filter(pk = goodid)
        print(good[0])
        goodList = Cart.objects.filter(good=good[0])
        print(goodList)
        if goodList.count() ==0:
            try:
                user = User.objects.get(user_token = h)
                ca = Cart.createCart(good[0],user)
                ca.createTime = timezone.now()
                ca.sum = good[0].price
                ca.save()
                ret['status'] = 1

                ordernum = user.carts.all().count()
                ret['ordernum'] = ordernum
            except Exception as e:
                print(e)
                return JsonResponse(ret)
            ret["status"] = 1
            return JsonResponse(ret)
        else:
            print(11111111111111111)
            ret["status"] = 2
            return JsonResponse(ret)
    return JsonResponse(ret)

#订单页面
def cart(request,pageid):
    user_token = request.session.get('user_token')
    try:
        h = User.objects.get(user_token=user_token)
        myorder = h.carts.all().order_by()
        print(myorder)
        leftSlider = FoodType.objects.order_by('typesort')
        print(type(pageid))
        paginator = Paginator(myorder, 8)
        page = paginator.page(pageid)
        last = page.number
        next = page.number
        if page.has_previous():
            last = page.previous_page_number()
        if page.has_next():
            next = page.next_page_number()
        ari = article.objects.all().order_by('-PV')
        arilist = ari[0:6]
        return render(request, 'gxGO/cart.html', {  'orders': page,
                                                    'arilist':arilist,
                                                    'leftSlider':leftSlider,
                                                    'user': h,
                                                    'page': page.number,
                                                    'allpage': paginator.num_pages,
                                                    'nextpage': next,
                                                    'lastpage': last
                                                    })
    except Exception as e:
        print(e)
        return redirect('myapp:index')


#删除购物车
def delete(request,id):
    user_token = request.session.get('user_token')
    try:
        car = Cart.objects.get(pk=id)
        user = User.objects.get(user_token=user_token)
        if car.buyer == user:
            car.delete()
            return redirect(reverse('market:cart', args=(1,)))
        else:
            return HttpResponse('非法操作')
    except Exception as e:
        print('11111111')
        return HttpResponse(e)
    return HttpResponse(id)
#删除订单
def delOr(request,id):
    user_token = request.session.get('user_token')
    try:
        order = Order.objects.get(pk=id)
        user = User.objects.get(user_token=user_token)
        if order.buyer == user:
            order.delete()
            return redirect(reverse('myapp:myorder', args=(1,)))
        else:
            return HttpResponse('非法操作')
    except Exception as e:
        print('11111111')
        return HttpResponse(e)
    return HttpResponse(id)
#购物数量
def add(request):
    h = request.session.get('user_token')
    ret = {"sum": 0,
           "num":0}
    if h:
        orderid = request.POST.get("goodNum")

        car = Cart.objects.filter(pk=orderid)[0]
        print(car)
        print(car.good.price)
        ornum = car.num
        print(ornum)

        met = request.POST.get("method")
        if met == '1':
            car.num = car.num + 1
        elif met == '0':
            car.num = car.num -1
            if car.num < 0:
                car.num = 0
        car.sum = car.num * car.good.price
        car.sum = round(car.sum,2)
        print(car.sum)
        car.save()
        ret = {"sumprice": car.sum,
               "num": car.num}
    return JsonResponse(ret)
#支付
def pay(request):
    h = request.session.get('user_token')
    ret = {"status": 0}
    if h:
        orderid = request.POST.get("goodNum")
        car = Cart.objects.filter(pk=orderid)[0]
        if car.sum != '0':
            order = Order.createOrder(car.good,car.buyer,car.num,car.sum)
            order.createTime = timezone.now()
            order.isSold = True
            order.save()
            car.delete()
            ret = {"status": 1}
    return JsonResponse(ret)
































