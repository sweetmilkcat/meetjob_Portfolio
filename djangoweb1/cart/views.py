from django.shortcuts import render,redirect

from django.http import HttpResponseRedirect

from cart import models

from product.models import shop

from django.utils.html import format_html

import os 
basedir = os.path.dirname(__file__) #抓取預設目錄位置
file = os.path.join(basedir,'ecpay_payment_sdk.py')
import importlib.util
spec = importlib.util.spec_from_file_location(
    "ecpay_payment_sdk",
    file
)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
from datetime import datetime

cartlist = list() #購物車的內容
customname ="" #客戶姓名
customphone = "" #客戶電話
customaddress = "" #客戶地址
customemail = "" #客戶email
orderTotal =0  #消費總額

goodsTitle = list() #存放入購物車的商品名稱

def addtocart(request,ctype=None,productid=None):
    global cartlist,itemsnum
    
    if ctype == "add": 
        product = shop.objects.get(id=productid) #會用get是因為帶入的產品ID一定有在資料表中
        flag = True #預設購物車中沒有相同的商品，表示購物車內這個商品不存在
        
        #檢查購物車中的商品是否有重複
        #unit[0]商品名稱 unit[1]價格 unit[2]數量 unit[3]價格*數量=總價
        for unit in cartlist:
            if product.title == unit[0]:  #表示有這個商品  
                unit[2] =str(int(unit[2]) + 1) #數量再加1 #
                unit[3] = str(int(unit[3]) + product.price) #累計金額
                
                flag = False #表示商品已經加入至購物車中
                break
        if flag: #再購物車中沒有此商品
            templist =list()
            templist.append(product.title)
            templist.append(str(product.price))
            templist.append('1')
            templist.append(str(product.price))
            cartlist.append(templist)#存放方式如[['nike','1000','1','1000'],['iphone','30000','2','60000']
            itemsnum = len(templist)
        
        request.session['cartlist'] = cartlist #將購物車內容存入到Session中 Session 是可以將資料儲存在伺服器端，當瀏覽器關閉時，資料就會被清除
        #content ={"cartlsit":cartlist,"itemsnum":itemsnum}
        return redirect('/shopping/') #跳轉至此網址
        #return render(request,'shopping.html',content)
    
    elif ctype =="update":#修改購物車數量
        n=0
        for unit in cartlist: #將購物車的內容抓出來，並修改數量和總價
            amount =request.POST.get('qty'+str(n),'1')#抓取 qty0,qty1,...,預設的數量是1
            if len(amount) ==0:
                amount='1'
            elif int(amount) <= 0:
                amount='1'
                
            unit[2] = amount 
            unit[3] = str( int(unit[1]) * int(unit[2]) )
            n+=1
        request.session['cartlist']=cartlist
        return redirect('/cart/')
    
    elif ctype=="empty":
        cartlist =list() #重新指向空的串列
        request.session['cartlist']=cartlist
        return redirect('/cart/')
    
    elif ctype == "remove":
        del cartlist[int(productid)] #將被的商品索引值刪除
        request.session['cartlist'] =cartlist
        return redirect('/cart/')
    
def cart(request): #顯示購物車內容
    global cartlist
    allcart = cartlist
    total =0 
    for unit in cartlist:
        total += int(unit[3])
    grandtotal = total +60 #預設運費為60元
    return render(request,'cart.html',locals())

def cartorder(request): 

    if "mymail" in request.session and "isAlive" in request.session:
        global cartlist,customname,customphone,customaddress,customemail
        total = 0
        allcart = cartlist
        for unit in cartlist:
            total += int(unit[3])
        grandtotal = total +60
        
        name = customname
        phone = customphone
        address =customaddress
        email = request.session['mymail']
        
        return render(request,'cartorder.html',locals())
    else:
        return HttpResponseRedirect("/login")
    
def cartok(request):
    global cartlist,customname,customphone,customaddress,customemail
    
    global orderTotal,goodsTitle
    
    total=0
    
    for unit in cartlist:
        total += int(unit[3])
    grandtotal = total +60
    
    orderTotal = grandtotal
    
    customname = request.POST.get('cuName','')
    customphone = request.POST.get('cuPhone','')
    customaddress = request.POST.get('cuAddr','')
    customemail = request.POST.get('cuEmail','')
    payType = request.POST.get('payType','')
    
    #新增資料至訂單資料表中
    #將物件建立起來後 unitorder用來存放物件資料，然後再丟到dorder中，好處是可以反查知到訂單中有多少資料
    unitorder = models.OrdersModel.objects.create(subtotal=total,shipping=60,grandtotal=grandtotal,customname=customname,customemail=customemail,customphone=customphone,customaddress=customaddress,paytype=payType)
    #將商品新增到明細表
    for unit in cartlist:
        goodsTitle.append(unit[0])#將要買的商品名稱新增到goodsTitle中
        #models.DetailModel =>指models.py 裡的DetailModel 函式
        #dorder=unitorder，透過unitorder建立的物件把資料
        total =int(unit[1])*int(unit[2])
        unitdetail = models.DetailModel.objects.create(dorder=unitorder,pname=unit[0],unitprice=unit[1],quantity=unit[2],dtotal=total)
    
    orderid = unitorder.id #取得訂單編號
    name = unitorder.customname
    email = unitorder.customemail
    cartlist = list() #因為結帳了所以購物車要清掉
    request.session['cartlist'] = cartlist
    
    if payType == "信用卡":
        return HttpResponseRedirect('/creditcard',locals())
    else:
        return render(request,'cartok.html',locals())
   # return render(request,'cartok.html',locals())
    return HttpResponseRedirect("/creditcard") #導至信用卡頁

#訂單完成後，可以做訂單查詢用
def cartordercheck(request):
    orderid = request.GET.get('orderid','')
    customemail = request.GET.get('customemail','')
    if orderid =='' and customemail == '':
        nosearch = 1
    else:
        order = models.OrdersModel.objects.filter(id=orderid).first() #抓第一筆資料
        if order == None:
            notfound = 1
        else:
            details = models.DetailModel.objects.filter(dorder=order)
    return render(request,"cartordercheck.html",locals())

def myorder(request):
    #判斷是否已經登入
    #抓出使用者的購買紀錄
    if "mymail" in request.session and "isAlive" in request.session:
        email = request.session['mymail']
        #不確定表單裡面有資料就要用filter ;確認表單中一定會有資料才能用get
        
        order = models.OrdersModel.objects.filter(customemail=email)
    else:
        return HttpResponseRedirect('/login')
    return render(request,"myorder.html",locals())

def ECpayCredit(request):
    global goodsTitle #要改內容就用global
    title = ""
    for i in goodsTitle:
        title += i +"#" #加#是因為商品若為多個時，要用#隔開
    order_params = {
        'MerchantTradeNo': datetime.now().strftime("NO%Y%m%d%H%M%S"),
        'StoreID': '',
        'MerchantTradeDate': datetime.now().strftime("%Y/%m/%d %H:%M:%S"),
        'PaymentType': 'aio',
        'TotalAmount': orderTotal,
        'TradeDesc': 'Meetjob-訂單',
        'ItemName': title,
        'ReturnURL': 'https://www.lccnet.com.tw/lccnet', #自己的網址，沒有可借用別人的
        'ChoosePayment': 'Credit',
        'ClientBackURL': 'https://www.lccnet.com.tw/lccnet',#自己的網址，沒有可借用別人的
        'ItemURL': 'https://www.ecpay.com.tw/item_url.php',
        'Remark': '交易備註',
        'ChooseSubPayment': '',
        'OrderResultURL': 'https://www.lccnet.com.tw/lccnet',#自己的網址，沒有可借用別人的
        'NeedExtraPaidInfo': 'Y',
        'DeviceSource': '',
        'IgnorePayment': '',
        'PlatformID': '',
        'InvoiceMark': 'N',
        'CustomField1': '',
        'CustomField2': '',
        'CustomField3': '',
        'CustomField4': '',
        'EncryptType': 1,
    }

    extend_params_1 = {
        'BindingCard': 0,
        'MerchantMemberID': '',
    }

    extend_params_2 = {
        'Redeem': 'N',
        'UnionPay': 0,
    }

    inv_params = {
        # 'RelateNumber': 'Tea0001', # 特店自訂編號
        # 'CustomerID': 'TEA_0000001', # 客戶編號
        # 'CustomerIdentifier': '53348111', # 統一編號
        # 'CustomerName': '客戶名稱',
        # 'CustomerAddr': '客戶地址',
        # 'CustomerPhone': '0912345678', # 客戶手機號碼
        # 'CustomerEmail': 'abc@ecpay.com.tw',
        # 'ClearanceMark': '2', # 通關方式
        # 'TaxType': '1', # 課稅類別
        # 'CarruerType': '', # 載具類別
        # 'CarruerNum': '', # 載具編號
        # 'Donation': '1', # 捐贈註記
        # 'LoveCode': '168001', # 捐贈碼
        # 'Print': '1',
        # 'InvoiceItemName': '測試商品1|測試商品2',
        # 'InvoiceItemCount': '2|3',
        # 'InvoiceItemWord': '個|包',
        # 'InvoiceItemPrice': '35|10',
        # 'InvoiceItemTaxType': '1|1',
        # 'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
        # 'DelayDay': '0', # 延遲天數
        # 'InvType': '07', # 字軌類別
    }

    # 建立實體
    ecpay_payment_sdk = module.ECPayPaymentSdk(
        MerchantID='2000132',
        HashKey='5294y06JbISpM5x9',
        HashIV='v77hoKGq4kWxNNIS'
    )

    # 合併延伸參數
    order_params.update(extend_params_1)
    order_params.update(extend_params_2)

    # 合併發票參數
    order_params.update(inv_params)

    try:
        # 產生綠界訂單所需參數
        final_order_params = ecpay_payment_sdk.create_order(order_params)

        # 產生 html 的 form 格式
        action_url = 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5'  # 測試環境
        # action_url = 'https://payment.ecpay.com.tw/Cashier/AioCheckOut/V5' # 正式環境
        html = ecpay_payment_sdk.gen_html_post_form(action_url, final_order_params)
        html = format_html(html) #格式化html,將文字的html轉換為網頁html
        return render(request,'paycredit.html',locals())
        #print(html) #原是列印出來 但不能在此列印 要在前台顯示
    except Exception as error:
        print('An exception happened: ' + str(error))