"""djangoweb1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from index.views import index
from question.views import question
from contact.views import contact
from reserve.views import reserve
from portfolio.views import portfolio
from aboutus.views import aboutus
from product.views import shopping
from service.views import nail

from cart.views import cart,addtocart,cartorder,cartok,cartordercheck,myorder,ECpayCredit
from member.views import login,logout,register,manage

urlpatterns = [
    path("admin/", admin.site.urls),
    path("",index),
    path("index/",index),
    path("portfolio/",portfolio),
    path("reserve/",reserve),#原預約頁籤，後先跟contact合併
    path("contact/",contact),
    path("question/",question),
    path("aboutus/",aboutus),
    path("shopping/",shopping),
    path("nail/",nail),
    path("cart/",cart),
    path("addtocart/<str:ctype>/",addtocart),
    path("addtocart/<str:ctype>/<int:productid>/",addtocart),
    path("cartorder/",cartorder), 
    path("cartok/",cartok),
    path("cartordercheck/",cartordercheck),
    path("login/",login),
    path("logout/",logout),
    path("register/",register),
    path("member/",manage),
    path("myorder/",myorder),
    path("creditcard/",ECpayCredit),
]
