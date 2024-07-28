from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomeUser(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    dob= models.DateField(null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True, unique=True) 
    usertype=models.CharField(max_length=200)
    certification=models.FileField(null=True,blank=True)
    address=models.CharField(null=True,blank=True,max_length=100)
    status=models.CharField(max_length=100,null=True, blank=True,default='pending')
    license=models.FileField(null=True,blank=True)
    Image=models.FileField(null=True,blank=True)
    certification = models.FileField(null=True, blank=True)
    # def __str__(self):
    #     return self.first_name


class medicine(models.Model):
    pharmacy_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    name = models.CharField(null=True, blank=True, max_length=100)
    price = models.IntegerField(null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=100)
    manufacturer =  models.CharField(null=True, blank=True, max_length=100)
    quantity = models.IntegerField(null=True, blank=True, unique=True)
    expiry_date = models.DateField()
    status= models.CharField(null=True, blank=True, max_length=100)
    brandname=models.CharField(null=True, blank=True, max_length=100)
    genericname=models.CharField(null=True, blank=True, max_length=100)
    strength=models.IntegerField(null=True, blank=True)
    Image=models.FileField(null=True,blank=True)
    
    
    # def __str__(self):
    #     return self.name
    
class cart(models.Model):
    medicine_id = models.ForeignKey(medicine, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=True, blank=True, unique=True)
 
class wishlist(models.Model):
    medicine_id = models.ForeignKey(medicine, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    cart_id = models.ForeignKey(cart, on_delete=models.CASCADE, null=True, blank=True)
  

class order(models.Model):    
    medicine_id = models.ForeignKey(medicine, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(cart, on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(null=True, blank=True, max_length=100, default='Pending')
    quantity = models.IntegerField(null=True, blank=True)
    payment_status = models.CharField(max_length=100, default='Pending')
    total_amount = models.IntegerField(null=True, blank=True)
    # def __str__(self):
    #     return self.name


class prescription(models.Model):
    name=models.CharField(null=True, blank=True, max_length=100)
    age = models.IntegerField(null=True, blank=True)
    address=models.CharField(null=True,blank=True,max_length=100)
    Date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(null=True, blank=True, max_length=100)
    user_id=models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    medicine_id = models.ForeignKey(medicine, on_delete=models.CASCADE)
    Dosage=models.CharField(max_length=50)
    prescription_file = models.FileField()
    quantity_prescribed = models.IntegerField()
