from django.db import models

# Create your models here.
class Portfolio(models.Model):
    title = models.CharField(max_length=100)
    link = models.CharField(max_length=255)
    
    class Meta:
        db_table = "portfolio"
        
class Newestimg(models.Model):
    title =models.CharField(max_length=50,blank=True,null=True)
    photolink = models.CharField(max_length=255,blank=True,null=True)
    create_date = models.DateField(auto_now_add=True,blank=True,null=True)
    
    class Meta:
        db_table = "newestimg"