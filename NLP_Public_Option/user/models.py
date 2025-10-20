from django.db import models

# Create your models here.

class TUser(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100,unique=True,verbose_name='用户名')
    password=models.CharField(max_length=200,verbose_name='密码')
    createtime = models.DateField(null=True, verbose_name="创建时间", )

    class Meta:
        db_table="t_user"
