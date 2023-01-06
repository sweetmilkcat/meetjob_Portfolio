from django.shortcuts import render
from .models import shop
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.
def shopping(request):
        goodsName=''
        sprice=''
        eprice=''
        if 'p' in request.GET:
            goodsName=request.GET['p']
            sprice=request.GET['priceS']
            eprice=request.GET['priceE']
            #只有產品名稱，但沒有價格範圍時
            if 'chk' in request.GET:
                chk =request.GET['chk']
                if (len(goodsName) >0 and len(sprice)==0 and len(eprice)==0) and len(chk) >0:
                    allGoods =shop.objects.filter(title__icontains =goodsName,ptype__icontains=chk).order_by('id')
                    
                elif (len(goodsName) ==0 and len(sprice)>0 and len(eprice) >0 ) and len(chk) >0:
                    allGoods= shop.objects.filter(price__gte =sprice,price__lte=eprice,ptype__icontains=chk).order_by('id')
                elif (len(goodsName) >0 and len(sprice)>0 and len(eprice) >0 ) and len(chk) >0:
                    allGoods= shop.objects.filter(title__icontains=goodsName,price__gte =sprice,price__lte=eprice,ptype__icontains=chk).order_by('id')
                else:
                    chk =request.GET['chk']
                    allGoods= shop.objects.filter(ptype__icontains=chk).order_by('id')
            else:        
                if (len(goodsName) >0 and len(sprice)==0 and len(eprice)==0):
                    allGoods =shop.objects.filter(title__icontains =goodsName).order_by('-id')
                elif (len(goodsName) ==0 and len(sprice)>0 and len(eprice) >0 ):
                    allGoods= shop.objects.filter(price__gte =sprice,price__lte=eprice).order_by('-id')
                elif (len(goodsName) >0 and len(sprice)>0 and len(eprice) >0 ):
                    allGoods= shop.objects.filter(title__icontains=goodsName,price__gte =sprice,price__lte=eprice).order_by('id')
                else:
                        allGoods = shop.objects.all().order_by('id')
        elif 'chk' in request.GET:
            chk =request.GET['chk']
            allGoods= shop.objects.filter(ptype__icontains=chk).order_by('id')
        else:
            allGoods = shop.objects.all().order_by('id')
            
        paginator = Paginator(allGoods,20)
        
        page =request.GET.get('page')
        
        try:
            allGoods = paginator.page(page)
        except PageNotAnInteger:
            allGoods = paginator.page(1)
        except EmptyPage:
            allGoods =paginator.page(paginator.num_pages)
        
        
        return render(request,"shopping.html",locals())