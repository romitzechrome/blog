from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class BlogPOST(models.Model):
    ID = models.AutoField(primary_key=True,null=False)
    title = models.CharField(max_length=200)
    body = models.CharField(max_length=200)
    auther = models.ForeignKey(User, on_delete=models.CASCADE)




