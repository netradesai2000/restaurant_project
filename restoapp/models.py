from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class dish(models.Model):
    name=models.CharField(max_length=50,verbose_name="Dish name")
    price=models.FloatField()
    dishdetails=models.CharField(max_length=100,verbose_name="Dish details")
    CAT=((1,'Maharashtrian Thali'),(2,'Punjabi Thali'),(3,'Chinese'))
    cat=models.IntegerField(verbose_name="category",choices=CAT)
    is_active=models.BooleanField(default=True,verbose_name="Availabel")
    pimage=models.ImageField(upload_to='image')
#def __str__(self):
    #return self.id

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    did=models.ForeignKey(dish,on_delete=models.CASCADE,db_column="did")
    qty=models.IntegerField(default=1)

class Order(models.Model):
    order_id=models.CharField(max_length=30)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column="uid")
    did=models.ForeignKey(dish,on_delete=models.CASCADE,db_column="did")
    qty=models.IntegerField(default=1)

class Contact(models.Model):
    uname=models.CharField(max_length=50)
    uemail=models.CharField(max_length=50)
    umsgs=models.CharField(max_length=200)
    
   
