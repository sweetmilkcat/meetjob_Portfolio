from django.shortcuts import render
from .models import custmessage
# Create your views here.
def contact(request):
    if 'username' in request.POST:
        username = request.POST['username']
        phone = request.POST['phone']
        email = request.POST['email']
        subject = request.POST['subject']
        message = request.POST['message']
        
        obj = custmessage.objects.create(username=username,phone=phone,email=email,subject=subject,message=message)
        
        obj.save()
    return render(request,"contact.html")