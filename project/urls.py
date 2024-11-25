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
    path('admin_login',views.admin_login,name='admin_login'),
    
    
    path('',views.index,name='index'),
    path('home',views.home,name='home'),
    path('Login',views.Login,name='Login'),
    path('Logout', views.Logout, name='Logout'),
    path('about_us',views.about_us,name='about_us'),
    
    path('password_reset/',views.password_reset_request, name='password_reset'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('set_new_password/', views.set_new_password, name='set_new_password'),
    
    #####user
    path('user_register',views.user_register,name='user_register'),
    path('user_medicine<int:id>',views.user_medicine,name='user_medicine'),
    path('medicine_view/<int:id>',views.medicine_view,name='medicine_view'),
    path('user_home',views.user_home,name='user_home'),
    path('search_medicines', views.search_medicines, name='search_medicines'),
    # path('search_phrmplace', views.search_phrmplace, name='search_phrmplace'),
    path('category_dropdown', views.category_dropdown, name='category_dropdown'),
    path('userprofile',views.userprofile,name='userprofile'),
    path('edit_profile',views.edit_profile,name='edit_profile'),
    path('wishlist_to_cart<int:id>',views.wishlist_to_cart,name='wishlist_to_cart'),
    # path('filteration_date',views.filteration_date,name='filteration_date'),
    path('help_page', views.help_page, name='help_page'),
    path('contact_us', views.contact_us, name='contact_us'),
    path('MEDICINE', views.MEDICINE, name='MEDICINE'),
    path('add_to_wishlist1/<int:id>/', views.add_to_wishlist1, name='add_to_wishlist1'),
    path('remove_to_wishlist1/<int:id>',views.remove_to_wishlist1,name='remove_to_wishlist1'),
    path('health_blog', views.health_blog, name='health_blog'),
    path('admin_product', views.admin_product, name='admin_product'),
    path('delivery_address', views.delivery_address, name='delivery_address'),
  
    
    

    
    
    
    
    #####prescription######
    
    # path('upload_prescription/<int:id>',views.upload_prescription, name='upload_prescription'),
   
    
    

    
    ####### user_cart ########
    path('add_to_cart/<int:id>', views.add_to_cart, name='add_to_cart'),
    path('cart_view', views.cart_view, name='cart_view'),
    path('remove_cart/<int:id>',views.remove_cart,name='remove_cart'),
    
    ####### user_wishlist ########

    path('add_to_wishlist/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_to_wishlist/<int:id>',views.remove_to_wishlist,name='remove_to_wishlist'),
    path('wishlist_view', views.wishlist_view, name='wishlist_view'),
    path('remove_wishlist<int:id>/', views.remove_wishlist, name='remove_wishlist'),
     ####### user_order ########
    path('order_history', views.order_history, name='order_history'),
    path('filteration',views.filteration,name='filteration'),
    path('order_item', views.order_item, name='order_item'),
    path('order_view', views.order_view, name='order_view'),
    path('payment_page/<int:am>', views.payment_page, name='payment_page'),
    # path('process_payment/', views.process_payment, name='process_payment'),
    # path('Debitcard', views.Debitcard, name='Debitcard'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    # path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    # path('order/<int:order_id>/review/', views.order_review, name='order_review'),
    # path('status/<int:id>', views.remove_order, name='remove_order'),
    # path('admin', views.admin, name='admin'),
   
    path('remove_orderview<int:id>/', views.remove_orderview, name='remove_orderview'),
    ######cardsystem####
    
    path('Debitcard', views.Debitcard, name='Debitcard'),
    
    
    #######cash on delivery#####
    path('cash_on_delivery', views.cash_on_delivery, name='cash_on_delivery'),
    
    
    path('payment_page', views.payment_page, name='payment_page'),
    path('search_medicines_scnd', views.search_medicines_scnd, name='search_medicines_scnd'),
    
    
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
    path('search_medicines_pharm', views.search_medicines_pharm, name='search_medicines_pharm'),
    path('user_medicine/<int:id>',views.user_medicine,name='user_medicine'),
    path('pharmacy_vieworder', views.pharmacy_vieworder, name='pharmacy_vieworder'),
    path('pharmacy_prescription', views.pharmacy_prescription, name='pharmacy_prescription'),
    path('pharmacy_history', views.pharmacy_history, name='pharmacy_history'),
    path('userorder_view/<int:id>', views.userorder_view, name='userorder_view'),
    path('chek_user_delivery/<int:id>', views.chek_user_delivery, name='chek_user_delivery'),
    path('search_delivery/<int:id>',views.search_delivery,name='search_delivery'),
    
    path('user_history_page',views.user_history_page,name='user_history_page'),
   path('view_eachPrdt<int:id>', views.view_eachPrdt, name='view_eachPrdt'),
   path('order_product/<int:id>', views.order_product, name='order_product'),
   path('pharmacy_pharmacy/<int:id>/<int:price>/<int:q>',views.pharmacy_pharmacy,name='pharmacy_pharmacy'),


    path('company_history', views.company_history, name='company_history'),

 ##### delivery###
 
 
  path('delivery_Register',views.delivery_Register,name='delivery_Register'),
  path('deliver_profile',views.deliver_profile,name='deliver_profile'),
   path('edit_delivery', views.edit_delivery, name='edit_delivery'),

  path('deliver_home', views.deliver_home, name='deliver_home'),
  path('delivr_order_user', views.delivr_order_user, name='delivr_order_user '),
  
path('delivery_available/<int:id>', views.delivery_available, name='delivery_available'),

path('delivery_order_view',views.delivery_order_view,name='delivery_order_view'),
  path('pharmacy_prescription', views.pharmacy_prescription, name='pharmacy_prescription'),
  
  
  
  
  
######html page link
path('delivr_wallect', views.delivr_wallect, name='delivr_wallect '),
path('delivr_history', views.delivr_history, name='delivr_history '),
#  path('delivr_wallect', views.delivr_wallect, name='delivr_wallect '),
path('status_delivery/<int:id>',views.status_delivery,name='status_delivery'),
path('Assign_delivery/<int:id>/<int:a>',views.Assign_delivery,name='Assign_delivery'),

 ##### company###
 
  path('company_Register',views.company_Register,name='company_Register'),
  path('company_profile',views.company_profile,name='company_profile'),
  path('company_edit', views.company_edit, name='company_edit'),
  path('company_home', views.company_home, name='company_home'),
  path('add_product', views.add_product, name='add_product'),
  path('product_view/<int:id>', views.product_view, name='product_view'),
  path('view_all', views.view_all, name='view_all'),
  path('delete_product/<int:id>', views.delete_product, name='delete_product'),
  path('edit_Product/<int:id>', views.edit_Product, name='edit_Product'),
  path('view_cpny_med', views.view_cpny_med, name='view_cpny_med'),
  path('company_status/<int:id>',views.company_status,name='company_status'),
  path('order_view_company',views.order_view_company,name='order_view_company'),
##########admin########
    path('admin_custumer', views.admin_custumer, name='admin_custumer'),
    path('admin_home', views.admin_home, name='admin_home'),
    # path('admin_pharmacy', views.admin_pharmacy, name='admin_pharmacy'),


    path('admin_delivery', views.admin_delivery, name='admin_delivery'),
    path('admin_view_custmer', views.admin_view_custmer, name='admin_view_custmer'),
    path('admin_view_pharmacy', views.admin_view_pharmacy, name='admin_view_pharmacy'),
    path('admin_delivery_view', views.admin_delivery_view, name='admin_delivery_view'),
    path('admin_pharmacy', views.admin_pharmacy, name='admin_pharmacy'),
    path('admin_user_view/<int:id>',views.admin_user_view,name='admin_user_view'),
    path('admin_pharmacy_view/<int:id>',views.admin_pharmacy_view,name='admin_pharmacy_view'),
    path('admin_delvry_viewone/<int:id>',views.admin_delvry_viewone,name='admin_delvry_viewone'),
    # path('admin_edit_viewone/<int:id>',views._vie,name='admin_edit_viewone'),

###edits:

    path('admin_edit_customer/<int:id>',views.admin_edit_customer,name='admin_edit_customer'),
    path('admin_edit_pharmacy/<int:id>',views.admin_edit_pharmacy,name='admin_edit_pharmacy'),
    path('admin_edit_delivery/<int:id>',views.admin_edit_delivery,name='admin_edit_delivery'),

    
    
    
    path('admin_delete_customer/<int:id>',views.admin_delete_customer,name='admin_delete_customer'),
    path('admin_delete_delivery/<int:id>',views.admin_delete_delivery,name='admin_delete_delivery'),
    path('admin_delete_pharmacy/<int:id>',views.admin_delete_pharmacy,name='admin_delete_pharmacy'),
    path('admin_category_list',views.admin_category_list,name='admin_category_list'),
    path('admin_add_category',views.admin_add_category,name='admin_add_category'),
    path('admin_delete_catagory/<int:id>',views.admin_delete_catagory,name='admin_delete_catagory'),
    path('admin_category_search',views.admin_category_search,name='admin_category_search'),
    path('admin_category_search',views.admin_category_search,name='admin_category_search'),
    path('admin_contact',views.admin_contact,name='admin_contact'),


]


if settings.DEBUG:
    
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)