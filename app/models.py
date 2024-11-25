from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomeUser(AbstractUser):
    age = models.IntegerField(null=True, blank=True)
    dob= models.DateField(null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True, unique=True) 
    usertype=models.CharField(max_length=200)
    address=models.CharField(null=True,blank=True,max_length=100)
    place=models.CharField(null=True,blank=True,max_length=500)
    status=models.CharField(max_length=100,null=True, blank=True,default='pending')
    license=models.FileField(null=True,blank=True)
    Image=models.FileField(null=True,blank=True)
    certificate = models.FileField(null=True, blank=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    delivery_address=models.CharField(null=True,blank=True,max_length=100)
    
    
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'  # Use email to log in instead of username
    REQUIRED_FIELDS = ['username', 'usertype']


class medicine(models.Model):
    pharmacy_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    name = models.CharField(null=True, blank=True, max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.CharField(null=True, blank=True, max_length=100)
    manufacturer =  models.CharField(null=True, blank=True, max_length=100)
    quantity = models.IntegerField(null=True, blank=True)
    expiry_date = models.DateField()
    status= models.CharField(null=True, blank=True, max_length=100)
    brandname=models.CharField(null=True, blank=True, max_length=100)
    genericname=models.CharField(null=True, blank=True, max_length=100)
    strength=models.IntegerField(null=True, blank=True)
    Image=models.FileField(null=True,blank=True)
    Image1=models.FileField(null=True,blank=True)
    Image2=models.FileField(null=True,blank=True)
    Image3=models.FileField(null=True,blank=True)
    category_name=models.CharField(max_length=100,null=True, blank=True)
    per_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    description1 = models.CharField(null=True, blank=True, max_length=1000)
    description2 = models.CharField(null=True, blank=True, max_length=1000)
    Image3=models.FileField(null=True,blank=True)
    def __str__(self):
        return self.name
    
class Category(models.Model):
    category_name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.category_name
    
class cart(models.Model):
    medicine_id = models.ForeignKey(medicine, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    added_date = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(null=True, blank=True)
    
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
    PAYMENT_STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('FAILED', 'Failed'),
    ]
    status = models.CharField(null=True, blank=True, max_length=100,choices=PAYMENT_STATUS_CHOICES,
        default='PENDING')
    quantity = models.IntegerField(null=True, blank=True)
    payment_status = models.CharField(max_length=100, default='booked')
    total_amount = models.IntegerField(null=True, blank=True)
    delivery_address=models.CharField(max_length=255)
    
    def __str__(self):
        return self.user_id.first_name
class order_review(models.Model):   
    medicine_id = models.ForeignKey(medicine, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    review = models.CharField(null=True,blank=True,max_length=100)
    rating = models.PositiveIntegerField(default=5)  
    Image=models.FileField(null=True,blank=True)
    review_date = models.DateTimeField(auto_now_add=True)
    # order=models.ForeignKey(order, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(cart, on_delete=models.CASCADE, null=True, blank=True)
    
class prescription(models.Model):
    name=models.CharField(null=True, blank=True, max_length=100)
    age = models.IntegerField(null=True, blank=True)
    address=models.CharField(null=True,blank=True,max_length=100)
    Date = models.DateTimeField(auto_now_add=True)
    user_id=models.ForeignKey(CustomeUser, on_delete=models.CASCADE,related_name='prescriptions_as_user')
    pharmancy_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE,related_name='prescriptions_as_pharmacy')
    prescription_file = models.FileField(null=True,blank=True)
    def __str__(self):
        return self.user_id.first_name
 
class product(models.Model):
    company_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    name = models.CharField(null=True, blank=True, max_length=100)
    price = models.IntegerField(null=True, blank=True)
    description = models.CharField(null=True, blank=True, max_length=100)
    quantity = models.IntegerField(null=True, blank=True, unique=True)
    Image=models.FileField(null=True,blank=True)
    Image1=models.FileField(null=True,blank=True)
    Image2=models.FileField(null=True,blank=True)
    Image3=models.FileField(null=True,blank=True)
    #  price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
 

    
class CompanyOrder(models.Model):
    company_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    
    medicine_id = models.ForeignKey(medicine, on_delete=models.CASCADE)
    product_id=models.ForeignKey(product,on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True, unique=True)


   
class Delivary(models.Model):
    delivary_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    place=models.CharField(max_length=500)
    age = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phonenumber = models.CharField(max_length=100)
    licence = models.FileField()
    image = models.FileField()
    dob= models.DateField(null=True, blank=True)

    STATUS_CHOICES = [
        ('available', 'available'),
        ('not available', 'not available'),
    ]

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name




class order_delivery(models.Model):
         pharmancy_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE,related_name='delivery_as_pharmacy')
         delivery_id=models.ForeignKey(Delivary, on_delete=models.CASCADE,related_name='delivery_as_delivery')
         order_id=models.ForeignKey(order, on_delete=models.CASCADE,related_name='delivery_as_order_id')
         status = models.CharField(max_length=50, choices=[
        ('pending', 'PENDING'),
        ('STARTED', 'started'),
        ('finished', 'finished'),
         ], default='pending')
    #    delivery_date
    # def __str__(self):
    #     return self.
 
class company_order(models.Model):
    pharmacy_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    product_id= models.ForeignKey(product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    total_amount = models.IntegerField(null=True, blank=True)
    PAYMENT_STATUS_CHOICES = [
            ('PENDING', 'Pending'),
            ('ACCEPT', 'accept'),
            ('REJECT', 'reject'),
        ]
    status = models.CharField(null=True, blank=True, max_length=100,choices=PAYMENT_STATUS_CHOICES,
            default='PENDING')
    
    from django.contrib.auth import get_user_model


class Notification(models.Model):
    user_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user

class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name