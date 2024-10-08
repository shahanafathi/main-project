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
    path('user_medicine<int:id>',views.user_medicine,name='user_medicine'),
    path('medicine_view/<int:id>',views.medicine_view,name='medicine_view'),
    path('user_home',views.user_home,name='user_home'),
    path('search_medicines/<int:id>', views.search_medicines, name='search_medicines'),
    path('search_phrmplace', views.search_phrmplace, name='search_phrmplace'),
    path('category_dropdown', views.category_dropdown, name='category_dropdown'),
    path('userprofile',views.userprofile,name='userprofile'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    # path('catgry',views.catgry,name='catgry'),
    # path('stock',views.stock,name='stock'),
    path('help_page', views.help_page, name='help_page'),

    
    
     
    
    #####prescription######
    
    path('upload_prescription/<int:id>',views.upload_prescription, name='upload_prescription'),
   
    
    

    
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
    path('payment_page/', views.payment_page, name='payment_page'),
    path('process_payment/', views.process_payment, name='process_payment'),
    # path('Debitcard', views.Debitcard, name='Debitcard'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    # path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    # path('order/<int:order_id>/review/', views.order_review, name='order_review'),
    # path('status/<int:id>', views.remove_order, name='remove_order'),
    path('admin', views.admin, name='admin'),
   
    path('remove_orderview<int:id>/', views.remove_orderview, name='remove_orderview'),
    ######cardsystem####
    
    path('Debitcard', views.Debitcard, name='Debitcard'),
    
    
    #######cash on delivery#####
    path('cash_on_delivery', views.cash_on_delivery, name='cash_on_delivery'),
    
    
    path('payment_page', views.payment_page, name='payment_page'),
    # path('order_review<int:id>', views.order_review, name='order_review'),
    
    
    ###pharmacyuser
    path('pharm_register',views.pharm_register,name='pharm_register'),
    path('pharm_profile',views.pharm_profile,name='pharm_profile'),
    path('edit_pharm',views.edit_pharm,name='edit_pharm'),
    path('pharm_home',views.pharm_home,name='pharm_home'),
    path('add_medicine', views.add_medicine, name='add_medicine'),
    path('edit_medicine/<int:id>', views.edit_medicine, name='edit_medicine'),
    path('medicine_viewss/<int:id>', views.medicine_viewss, name='medicine_viewss'),
     path('medicine_viewpharma', views.medicine_viewpharma, name='medicine_viewpharma'),
    path('delete_med/<int:id>',views.delete_med,name='delete_med'),
    # path('search_medicine',views.search_medicine,name='search_medicine'),
    path('user_medicine/<int:id>',views.user_medicine,name='user_medicine'),
    path('pharmacy_vieworder', views.pharmacy_vieworder, name='pharmacy_vieworder'),
    # path('pharmacy_viewcompany', views.pharmacy_viewcompany, name='pharmacy_viewcompany'),
    path('pharmacy_history', views.pharmacy_history, name='pharmacy_history'),
    path('pharmacy_userhistory', views.pharmacy_userhistory, name='pharmacy_userhistory'),
     path('userorder_view/<int:id>', views.userorder_view, name='userorder_view'),
 
 
 ##### delivery###
 
  path('delivery_Register',views.delivery_Register,name='delivery_Register'),
  path('deliver_profile',views.deliver_profile,name='deliver_profile'),
  path('deliver_home', views.deliver_home, name='deliver_home'),
  path('delivr_order_user', views.delivr_order_user, name='delivr_order_user '),
# path('history', views.history, name='history '),
# path('delivery_review', views.delivery_review, name='delivery_review '),

 
 ##### company###
 
  path('company_Register',views.company_Register,name='company_Register'),
  path('company_profile',views.company_profile,name='company_profile'),
  path('company_edit', views.company_edit, name='company_edit'),
  path('company_home', views.company_home, name='company_home '),

##########admin########
# path('adminhome', views.adminhome, name='adminhome'),



]


if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)