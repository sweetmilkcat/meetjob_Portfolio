from django.db import models

# Create your models here.
class shop(models.Model):
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    link = models.CharField(max_length=255)
    photo = models.CharField(max_length=255)
    ptype = models.CharField(max_length=20,default=0)
    create_date = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'shop'