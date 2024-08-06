"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf .urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('home',views.home,name='home'),
    path('Login',views.Login,name='Login'),
    path('logout', views.logout, name='logout'),
    #####user
    path('user_register',views.user_register,name='user_register'),
    path('user_home',views.user_home,name='user_home'),
    path('search_medicines', views.search_medicines, name='search_medicines'),
    path('userprofile',views.userprofile,name='userprofile'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    
    ####### user_cart ########
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('cart_view', views.cart_view, name='cart_view'),
    path('remove_cart/<int:id>',views.remove_cart,name='remove_cart'),
    
    ####### user_wishlist ########

    path('add_to_wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist_view', views.wishlist_view, name='wishlist_view'),
    path('remove_wishlist<int:id>/', views.remove_wishlist, name='remove_wishlist'),
     ####### user_order ########

    path('order_item', views.order_item, name='order_item'),
    path('order_view', views.order_view, name='order_view'),
    # path('status/<int:id>', views.remove_order, name='remove_order'),
    path('admin', views.admin, name='admin'),
    path('add_category',views. add_category, name='add_category'),
     path('view_Category',views. view_Category, name='view_Category'),
    
    
    ###Epharmacyuser
    path('pharm_register',views.pharm_register,name='pharm_register'),
    path('pharm_profile',views.pharm_profile,name='pharm_profile'),
    path('edit_pharm',views.edit_pharm,name='edit_pharm'),
    path('pharm_home',views.pharm_home,name='pharm_home'),
    path('add_medicine', views.add_medicine, name='add_medicine'),
    path('edit_medicine/<int:id>', views.edit_medicine, name='edit_medicine'),
     path('medicine_view/<int:id>', views.medicine_view, name='medicine_view'),
    path('delete_med/<int:id>',views.delete_med,name='delete_med'),
    # path('search_medicine',views.search_medicine,name='search_medicine'),
    path('user_medicine/<int:id>',views.user_medicine,name='user_medicine'),
    path('pharmacy_vieworder', views.pharmacy_vieworder, name='pharmacy_vieworder'),
    

    
 
 
 ##### delivery###
 
 path('delivery_Register',views.delivery_Register,name='delivery_Register'),
  path('deliver_profile',views.deliver_profile,name='deliver_profile'),
 

]


if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)