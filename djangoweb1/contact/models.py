from django.db import models

# Create your models here.
class custmessage(models.Model):
    username = models.CharField(max_length=40)
    phone = models.CharField(max_length=10)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=255)
    create_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'custmessage'