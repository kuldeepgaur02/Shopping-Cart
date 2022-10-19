from email import message
from pyexpat import model
from statistics import mode
from django.db import models

# Create your models here.

class product(models.Model):# inheriting from model
    product_id =models.AutoField#Autofeild does auto increment 
    product_name = models.CharField(max_length=50)# providing name of the product 
    category=models.CharField(max_length=50,default='')
    subcategory=models.CharField(max_length=50,default='')
    price=models.IntegerField(default="0")
    desc = models.CharField(max_length=300)
    pub_date=models.DateField()
    image=models.ImageField(upload_to="blog/images",default='')
    
    def __str__(self):
        return self.product_name
    
# Taking contact details from the users 

    
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=70, default="")
    number = models.CharField(max_length=70, default="")
    message = models.CharField(max_length=500, default="")


    def __str__(self):
        return self.name


class Orders(models.Model):
    order_id=models.AutoField(primary_key=True)
    items_json=models.CharField(max_length=5000)
    name=models.CharField(max_length=90)
    email=models.CharField(max_length=111)
    address= models.CharField(max_length=111)
    city=models.CharField(max_length=111)
    state=models.CharField(max_length=111)
    zip_code=models.CharField(max_length=111)
    phone = models.CharField(max_length=111,default='')
  
        
    
class OrderUpdates(models.Model):
    update_id=models.AutoField(primary_key=True)
    order_id=models.IntegerField(default='')
    update_desc= models.CharField(max_length=5000)
    timestamp=models.DateField(auto_now_add=True)#will giver current time span if not provided
def __str__(self):
    return self.upadte_desc[0:7]+'...'
    