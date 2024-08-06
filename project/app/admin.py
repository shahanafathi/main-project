from django.contrib import admin
from .models import CustomeUser,medicine,cart,wishlist,order,Category

# Register your models here.
admin.site.register(CustomeUser)
admin.site.register(cart)
admin.site.register(wishlist)
admin.site.register(order)
admin.site.register(Category)
