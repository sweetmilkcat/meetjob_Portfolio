from django.shortcuts import render
from .models import Portfolio,Newestimg
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger

# Create your views here.
def portfolio(request):
    
    newimg = Newestimg.objects.all().order_by('-create_date')
    category1 = Portfolio.objects.filter(title__contains='上班')[:12]
    category2 = Portfolio.objects.filter(title__contains='新娘')[:12]
    category3 = Portfolio.objects.filter(title__contains='學生')[:12]
    typename=''
    title=''
    if 'keyword' in request.GET:
        title = request.GET['keyword']
        
        if len(title) >0 :
            data = Portfolio.objects.filter(title__contains=title).order_by('-id')
        else:
            data = Portfolio.objects.filter(title__contains='氣質')[:4]
    elif 'type' in request.GET:
        typename = request.GET['type']
        if len(typename) >0:
            data = Portfolio.objects.filter(title__contains=typename).order_by('-id')
        else:
            data = Portfolio.objects.all().order_by('-id')
    else:
        data = Portfolio.objects.all().order_by('-id')
    paginator = Paginator(data,12)
    page = request.GET.get('page')
    
    try:
        pageData = paginator.page(page)
    except PageNotAnInteger:
        pageData = paginator.page(1)
    except EmptyPage:
        pageData = paginator.page(paginator.num_pages)
        
    is_paginated = True if paginator.num_pages > 1 else False # 如果页数小于1不使用分页
        
    #查詢
    
    #採用字典方式傳送至網頁
    content = {"photolist":pageData,'is_paginated': is_paginated,"category1":category1,"category2":category2,"category3":category3,"newimg":newimg}
    
    return render(request,"portfolio.html",content)