from django.contrib import admin
from .models import CustomeUser,medicine,cart,wishlist,order,Category,prescription,Delivary,order_delivery,company_order

# Register your models here.
admin.site.register(CustomeUser)
admin.site.register(cart)
admin.site.register(wishlist)
admin.site.register(order)
admin.site.register(Category)
admin.site.register(prescription)
admin.site.register(Delivary)
admin.site.register(medicine)
admin.site.register(order_delivery)
admin.site.register(company_order)