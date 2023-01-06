from django.db import models

# Create your models here.
class OrdersModel(models.Model):
    subtotal = models.IntegerField(default=0)
    shipping = models.IntegerField(default=0)
    grandtotal = models.IntegerField(default=0)
    customname = models.CharField(max_length=100)
    customemail = models.CharField(max_length=100)
    customphone = models.CharField(max_length=50)
    paytype = models.CharField(max_length=20)
    create_date = models.DateTimeField(auto_now_add=True)
    customaddress = models.CharField(max_length=200)
    
    def __str__(self):#不指定資料表名稱，而是由系統自動建立
        return self.customname

class DetailModel(models.Model):
    #dorder 中的值是來至於"外來鍵"
    dorder = models.ForeignKey('OrdersModel',on_delete=models.CASCADE)     
    pname = models.CharField(max_length=100)
    unitprice = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    dtotal = models.IntegerField(default=0)
    
    def __str__(self):
        return self.pname