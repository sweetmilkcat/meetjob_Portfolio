from django.db import models
"""
新增欄位時會出現 :[It is impossible to add a non-nullable field 'activity_starts' to activity without specifying a default. This is because the database needs something to populate existing rows.]的訊息
因之前欄位已經有先創建，再重新創建會因為欄位預設不可為空值出現錯誤
所以在新增的欄位加上以下兩個設定值
blank=True,null=True 
例如:activity_starts = models.CharField(max_length=8,blank=True,null=True)
"""
# Create your models here.
class activity(models.Model):
    title = models.CharField(max_length=50)
    activity_starts = models.CharField(max_length=8,default=0)
    activity_end = models.CharField(max_length=8,null=True,default=0)
    content = models.CharField(max_length=255)
    photo = models.CharField(max_length=255)
    create_date = models.DateField(auto_now=True)
    
    class Meta:
        db_table = "actibity"