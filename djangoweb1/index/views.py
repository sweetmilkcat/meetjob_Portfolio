from django.shortcuts import render
from .models import activity
# Create your views here.
#request 上網用的
#return render(request,'index.html') render(使用者個回應，對應到哪個html)
def index(request):
    poster1 = activity.objects.all()[:1]
    poster2 = activity.objects.all()[1:2]
    content = {"poster1":poster1,"poster2":poster2}
    
    return render(request,'index.html',content)