from django.shortcuts import render
import hashlib
from .models import Member
from django.http import HttpResponseRedirect
# Create your views here.
def login(request):
    msg =""
    if 'email' in request.POST:
        email = request.POST['email']
        password = request.POST['password']
        password = hashlib.sha3_256(password.encode('utf-8')).hexdigest()
        
        obj = Member.objects.filter(email=email,password=password).count()
        
        if obj >0 : #表示資料表中有這個使用者，且帳密都正確
            #建立SESSION 物件，可以將值 暫時存在伺服器端，當瀏覽器關閉時，SESSION內的值就會不見，重開瀏覽器時，就會抓不到值
            #打開瀏覽器時，他會主動跟伺服器抓取一個ID，每次ID會不同
            #儲存在本地端電腦的，稱為COOKIES
            request.session['mymail'] =email #儲存SESSION資料，其中mymail是自取可以自由更改
            request.session['isAlive'] =True
            
            #加上Cookie 功能，若使用者進用時就會失效
            #宣告Cookie的物件
            response = HttpResponseRedirect('/')
            
            #設定存放email的值， max_age=1200 指的是存活時間(1200秒)
            response.set_cookie("UMail",email,max_age=1200)
            
            
            return HttpResponseRedirect('/index') #指向根目錄(首頁)
        else:
            msg = "帳密錯誤，請重新輸入"
            return render(request,'login.html',locals())
    else:
        if "mymail" in request.session and "isAlive" in request.session:
            return HttpResponseRedirect("/member")
        else: #抓cookie 
            myemail =  request.COOKIES.get("Umail","" )#抓取Cookie 的值，若沒有則空白
            return render(request,'login.html',locals())

def logout(request):
    del request.session["isAlive"] #刪除login的資料
    del request.session["mymail"]
    
    #刪除cookie，做跳轉
    response = HttpResponseRedirect('/login')
    
    response.delete_cookie("UMail")
    #另一種寫法(不做跳轉)，記得上面要import HttpResponse
    #response = HttpResponse("Delete Cookie")
    #response.delete_cookie("UMail")
    return HttpResponseRedirect('/login')

def register(request):
    msg =""
    #如果是用表單的方式送出資料的話，就接收送過來的資料
    if 'userName' in request.POST:
        username = request.POST['userName']
        email =  request.POST['email']
        password = request.POST['pwd']
        sex = request.POST['sex']
        birthday = request.POST['birthday']
        address = request.POST['address']
        
        # password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        password = hashlib.sha3_256(password.encode('utf-8')).hexdigest() #sha3_256 是版本更高的加密
        obj = Member.objects.filter(email=email).count()#回傳筆數
        if obj ==0: #表示這個email沒有註冊過
        #新增會員資料
            Member.objects.create(name=username,sex=sex,birthday=birthday,email=email,password=password,address=address)
            msg ="恭喜你，已完成註冊"
        else:
            msg = "此Email已存在，請換一個mail註冊"
    return render(request,'register.html',locals())

def manage(request):
    #要判斷是否已經登入了，若沒有就要導回去登入
    if "mymail" in request.session and "isAlive" in request.session:
        msg=''
        if "oldpwd"  in request.POST:
            oldpwd = request.POST['oldpwd']
            newpwd = request.POST['newpwd']
            #先將2個密碼加密
            oldpwd = hashlib.sha3_256(oldpwd.encode('utf-8')).hexdigest()
            newpwd = hashlib.sha3_256(newpwd.encode('utf-8')).hexdigest()
            email = request.session['mymail']
            #確認使用者輸入的舊密碼是否正確
            obj = Member.objects.filter(email=email,password=oldpwd).count()
            if obj >0:
                #更新密碼，將資料抓出來為物件
                user = Member.objects.get(email=email)
                user.password = newpwd
                user.save()
                msg = "密碼變更完成"
            else:
                msg ="舊密碼不正確，請重新輸入"
             
        return render(request,'manage.html',locals())
    else:
        return HttpResponseRedirect('/login')