from . import views
from django.urls import re_path
app_name ='[market]'
urlpatterns = [
    re_path('^(\d+)/(\d+)/(\d+)/(\d+)/$',views.shop,name = 'shop'),
    re_path('^cart_ajax/$',views.cart_ajax,name = 'cart_ajax'),
    re_path('^cart/(\d+)/$',views.cart,name = 'cart'),
    re_path('^delete/(\d+)/$',views.delete,name = 'delete'),
    re_path('^delOr/(\d+)/$',views.delOr,name = 'delOr'),
    re_path('^add/',views.add,name = 'add'),
    re_path('^pay/',views.pay,name = 'pay'),
]

