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
    contact_name = models.CharField(max_length=255, null=True, blank=True)
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
    category_name=models.CharField(max_length=100,null=True, blank=True)
    
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
    
    # def __str__(self):
    #     return self.name
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
 
    

    # def total_price(self):
    #     return self.quantity * self.unit_price
    
# class company_product(models.Model):
#     company_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
#     product_name = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock_quantity = models.IntegerField()
    
    
class CompanyOrder(models.Model):
    company_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled')
    ], default='pending')
       
    medicine_id = models.ForeignKey(medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True, unique=True)
# class PharmacyOrderToCompany(models.Model):
#     pharmacy_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)  # Assuming the pharmacy is represented by a user model
#     company_id = models.ForeignKey(CustomeUser, on_delete=models.CASCADE)
#     order_date = models.DateTimeField(auto_now_add=True)
#     total_amount = models.DecimalField(max_digits=10,)
#     status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')])

# class PharmacyOrderToCompanyDetail(models.Model):
#     order = models.ForeignKey(PharmacyOrderToCompany, related_name='order_details', on_delete=models.CASCADE)
#     product_id = models.ForeignKey(company_product, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     price = models.IntegerField(null=True, blank=True, unique=True)
#     quantity = models.IntegerField(null=True, blank=True, unique=True)