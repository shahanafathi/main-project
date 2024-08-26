from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from .models import CustomeUser,medicine,cart,order,wishlist,Category,CompanyOrder
# from django.shortcuts import get


from django.urls import reverse
from django.contrib import messages

# Create your views here.

def index(request):
     return redirect(home)
def home(request):
      return render(request,'home.html')
# ***************main login******

def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
         # Authenticate superusers (admins)
        print(user)
         
        admin_user = authenticate(request, username=username, password=password)
        if admin_user is not None and admin_user.is_staff:
            login(request, admin_user)
             # Authenticate superusers (admins)
            # return redirect(admin_profile)  # Redirect to the admin dashboard
        elif user is not None:
            # If not an admin, check regular users
            login(request, user)
            if user.usertype == "user":     #user profile
                return redirect(user_home)
            elif user.usertype == "pharmacy":
                return redirect(pharm_home)
            elif user.usertype == "delivery":
                return redirect(deliver_home)
            elif user.usertype == "doctor":
                return redirect(doctor_profile)
            elif user.usertype == "company":
                return redirect(company_profile)
            elif user.usertype=="admin":
                # return HttpResponse('homepage sucess')
                  return redirect('/admin/')
            return render(request, 'login.html', context)
        else:
            context = {
                'message': "Invalid credentials"
            }
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')
      
        

# def Login(request):
#     if request.method == "POST":
#         Username = request.POST['username']
#         Password = request.POST['password']
#         admin_user = auth.authenticate(request,username=Username,password=Password)
#         if admin_user is not None and admin_user.is_staff:
#             auth.login(request,admin_user)
#             # return redirect('/admin/')  # Redirect to the admin dashboard
#             return redirect(admin)
        
#         data = auth.authenticate(username=Username,password=Password)
#         if data is not None:
#             auth.login(request,data)
#             if data.usertype == "user" :
#              return redirect(user_home)
#             if data.usertype == "pharmacy" and data.status == "approved":
#                 return redirect(pharm_home)
#             if data.usertype == "pharmacy" and data.status == "pending":
#                 return HttpResponse("Can't login without approval of admin.Either wait for 1 day or register again")   
#             # elif data.usertype == "deliver" and data.status == "pending":
#             #     return HttpResponse("Can't login without approval of admin.Either wait for 1 day or register again")
#             # elif data.usertype == "deliver" and data.status == "accept":
#             #     return redirect(deliver_profile)
            
#             else:
#                 context ={
#                     'message': "Invalid credentials"
#                     }
#                 return render(request, 'login.html', context)

#     # Render the login form for GET requests
#     else:
#       return render(request, 'login.html')


def logout(request):
    auth.logout(request)
    return redirect(Login)



#*************user**************

def user_register(request):
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['Email']
            if CustomeUser.objects.filter(email=email).exists():
             return render(request,'user/register.html',{'error':'email already exists'})
            address = request.POST['Address']
            DOB = request.POST['DOB']
            phoneno = request.POST['Phonenumber']
            if CustomeUser.objects.filter(phone_number=phoneno).exists():
             return render(request,'user/register.html',{'error':'Phonenumber already exists'})
            age = request.POST['Age']
            username = request.POST['UserName']
            if CustomeUser.objects.filter(username=username).exists():
             return render(request,'user/register.html',{'error':'username already exists'})
            # password = make_password(request.POST['Password'])
            password =request.POST['Password']
            Confirmpassword=request.POST['Confirmpassword']
            if password!=Confirmpassword:
             return render(request,'user/register.html',{'error':'password not matching'})
            data=CustomeUser.objects.create_user(first_name=name,email=email,address=address,age=age,phone_number=phoneno,dob=DOB,password=password,username=username,usertype='user')
            data.save()
            # return HttpResponse('sucess')
            return render(request,'login.html')
        
            # return redirect(userhome)
        else:
            return render(request,'user/register.html')

def userprofile(request):
    users=CustomeUser.objects.get(id=request.user.id)
    return render(request,'user/profile.html',{'data':users})

def edit_profile(request):
    data=CustomeUser.objects.get(id=request.user.id)
    if request.method=='POST':
        data.first_name=request.POST['Name']
        data.age=request.POST['age']
        data.Phonenumber=request.POST['Phonenumber']
        data.DOB=request.POST['DOB']
        data.Address=request.POST['Address']
        data.email=request.POST['Email']  
        data.username=request.POST['UserName']
        data.save()
        return redirect(userprofile)
    else:
        return render(request,'user/editprofile.html',{'datas':data})
       

def user_home(request):
    medicines =medicine.objects.all()
    return render(request, 'user/userhome.html', {'medicines': medicines})
    
def search_medicines(request):
    if request.method=='POST':
        Search=request.POST['search']
        data = medicine.objects.filter(name__icontains=Search)
        return render(request,'user/userhome.html',{'datas': data,'search': Search})
    else:
        return redirect(user_home)

# def search_medicines(request):
#     if request.method=='POST':
#         Search=request.POST.get('search','')
#         data = medicine.objects.filter(name__icontains=Search)
#         return render(request,'user/userhome.html',{'datas': data,'search': Search})
#     else:
#         # return redirect(user_home)
#             return render(request,'user/userhome.html',{'datas': data,'search': Search})
  
  
def search_medicines(request):
    if request.method == 'POST':
        search_query = request.POST.get('search', '')
        medicines = medicine.objects.filter(name__icontains=search_query)
        return render(request, 'user/userhome.html', {'medicines': medicines, 'search_query': search_query})
    else: 
        return render(request, 'user/userhome.html', {'medicines': medicine.objects.all()})
  
def user_medicine(request,id):
    medicines = medicine.objects.get(id=id)
    return render(request, 'user/user_medicine.html', {'medicines': medicines})

#########  user cart#######

# def add_to_cart(request, id):
#     user = CustomeUser.objects.get(id=request.user.id)
#     medicine_item = medicine.objects.get(id=id)
#     cart_items = cart.objects.filter(user_id=user)  # Filter by current user

#     # Check if the medicine is already in the cart
#     if cart.objects.filter(medicine_id=medicine_item, user_id=user).exists():
#         return render(request, 'user/cartview.html', {
#             'message': 'This item already exists in your cart',
#             'cart_items': cart_items
#         })
#     else:
    
#         # Add the medicine to the cart
#         cart.objects.create(medicine_id=medicine_item, user_id=user)
#         return redirect('cart_view')  # Redirect to cart view

def add_to_cart(request, id):
    datas = CustomeUser.objects.get(id=request.user.id)
    medicine_item = medicine.objects.get(id=id)
    cart_items = cart.objects.all()
    if cart.objects.filter(medicine_id=medicine_item, user_id=datas).exists():
        return render(request, 'user/cartview.html', {'message': 'This item already exists in your cart', 'cart_items': cart_items})
    else:
        cart_add = cart.objects.create(medicine_id=medicine_item, user_id=datas)
        cart_add.save()
        return redirect('cart_view') 
    
def cart_view(request):
    # cart_items = cart.objects.filter(user_id=request.user.id)
    cart_items = cart.objects.all()
    # print(cart_items)
    return render(request, 'user/cartview.html', {'cart_items': cart_items})


def cart_view(request):
    user = request.user
    cart_items = cart.objects.filter(user_id=user)  # Filter cart items by current user
    return render(request, 'user/cartview.html', {'cart_items': cart_items})

def remove_cart(request, id):
    user = request.user
    # Delete the specific cart item for the current user
    cart.objects.filter(id=id, user_id=user).delete()
    # return redirect('cart_view')  # Redirect to cart view


def remove_cart(request,id):
   
    cart_del =  cart.objects.get(id=id)
    cart_del.delete()
    return redirect(cart_view)

######## wishlist#######
def add_to_wishlist(request, id):
    datas = CustomeUser.objects.get(id=request.user.id)
    print(datas)
    medicine_item = medicine.objects.get(id=id)
    wishlist_add = wishlist.objects.create(medicine_id=medicine_item,user_id=datas)
    wishlist_add.save()
    return redirect(wishlist_view)
    # return HttpResponse('sucess')
    # return render(request, 'user/wishlist1.html', {'item': medicine_item, 'datas': datas,'item':wishlist_add})


def wishlist_view(request):
    wishlist_items = wishlist.objects.filter(user_id=request.user.id)
    # wishlist_items = wishlist.objects.all()
    # print(wishlist_items)
    return render(request,'user/wishlist1.html', {'wishlist': wishlist_items})

def remove_wishlist(request,id):
    wishlist_del = wishlist.objects.get(id=id)
    wishlist_del.delete()
    return redirect( wishlist_view)
######## order list####
def order_item(request):
    datas=CustomeUser.objects.get(id=request.user.id)
    cart_item = cart.objects.filter(user_id=datas)
    # var=order.objects.filter(user_id=datas)
    Ttl_amounts=0
    
    for item in cart_item:
        total_amt=(item.medicine_id.price*item.medicine_id.quantity)
        Ttl_amounts += total_amt
        order_item=order.objects.create(user_id=datas,medicine_id=item.medicine_id,total_amount=total_amt, quantity=item.quantity)
        order_item.save()
        # return redirect( order_view)
        # return redirect(process_payment)
        return render(request,'user/order.html', {'order_item':cart_item,'total_amounts':Ttl_amounts})

def payment_page(request):
    # user = request.user
    user = CustomeUser.objects.get(id=request.user.id)
    cart_items = cart.objects.filter(user_id=user)
    # total_price = sum(item.medicine_id.price * item.quantity for item in cart_items)
    return render(request, 'user/payment.html', {'cart_items': cart_items})

def process_cod_payment(request):
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address')
        if not delivery_address:
            messages.error(request, "Please provide a delivery address.")
            return redirect('cod_payment_page')
# def process_payment(request):
#     if request.method == 'POST':
#         # pharmacy = CustomeUser.objects.get(id=id)
#         total_amount = request.POST.get('total_amount')
#         payment_method = request.POST.get('payment_method')

#         # order = order.objects.create(pharmacy=pharmacy,user=request.user,total_amount=total_amount,payment_method=payment_method,status='Pending')
#         order.save()
#         return redirect('order_success')
#     else:
#         #  return render(request, 'order/create_order.html')
#         return redirect('order_confirmation')

def process_payment(request):
    if request.method == 'POST':
        # Simulate payment processing
        cardholder_name = request.POST.get('cardholder_name')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        
        

        # Implement actual payment processing here
        # e.g., using Stripe, PayPal, etc.

        # Assuming payment is successful
        # Redirect to order confirmation page
        return redirect('order_confirmation')
    
    else:
        return redirect(payment_page)



def order_confirmation(request):
    datas = CustomeUser.objects.get(id=request.user.id)
    # order_items = order.objects.filter(user_id=datas)
    cart_items = cart.objects.filter(user_id=datas)
    cart_items.delete()
    # if order_item is sucess
    return render(request, 'user/order_confirmation.html',{'cart_items': cart_items})


def order_view(request):
    datas = CustomeUser.objects.get(id=request.user.id)
    order_items = order.objects.filter(user_id=datas)
    # order_items = order.objects.all()order_items
    for item in order_items:
     total_amounts = item.total_amount  # Calculate total for display
    # return render(request, 'user/.html', {'order_items': order_items})
    return render(request, 'user/order1.html', {'order_items': order_items})

# def order_review(request):
#     datas = CustomeUser.objects.get(id=request.user.id)
#     order_items = order.objects.filter(user_id=datas)
#     exst_review=order.objects.filter(user=datas, order_items =order).exists()
#     if exst_review:
#         return HttpResponse("You have already reviewed this order or exists.")
#     if request.method == "POST":
#         review_text = request.POST.get("review")
#         rating = request.POST.get("rating")  # Default rating to 5 if not provided
#         image = request.FILES.get('image')
#         review=order.object.create
























































#   #***********pharmacy**********

def view_Category(request):
        categories = Category.objects.all()
        return render(request, 'pharmacy/ctgory.html', {'categories': categories})
        
def add_category(request):
    if request.method == "POST":
        ctgry_name = request.POST['category_name']
        if not Category.objects.filter(category_name=ctgry_name).exists():
            Category.objects.create(category_name=ctgry_name)
            message = "Category added successfully."
        else:
            message = "Category already exists."
        return render(request, 'pharmacy/categery.html', context={'add': message})
    else:
        return render(request,'pharmacy/categery.html')





        
def pharm_register(request):
    if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['Email']
            if CustomeUser.objects.filter(email=email).exists():
             return render(request,'pharmacy/registerp.html',{'error':'email already exists'})
            address = request.POST['Address']
           
            phoneno = request.POST['Phonenumber']
            if CustomeUser.objects.filter(phone_number=phoneno).exists():
             return render(request,'pharmacy/registerp.html',{'error':'username already exists'})
            username = request.POST['UserName']
            if CustomeUser.objects.filter(username=username).exists():
             return render(request,'pharmacy/registerp.html',{'error':'username already exists'})
            password = request.POST['Password']
            Confirmpassword=request.POST['Confirmpassword']
            if password!=Confirmpassword:
             return render(request,'pharmacy/registerp.html',{'error':'password not matching'})
            data=CustomeUser.objects.create_user(first_name=name,email=email,address=address,phone_number=phoneno,password=password,username=username,usertype='pharmacy')
            data.save()
            return render(request,'login.html')
    else:
           return render(request,'pharmacy/registerp.html')
            # return HttpResponse('sucess it')
            #  return render(request,'login.html')


def pharm_profile(request):
    user=CustomeUser.objects.get(id=request.user.id)
    return render(request,'pharmacy/profilep.html',{'data':user})



def edit_pharm(request):
    data=CustomeUser.objects.get(id=request.user.id)
    if request.method=='POST':
        data.first_name=request.POST['Name']
        data.age=request.POST['age']
        data.Phone_number=request.POST['Phonenumber']
        data.dob=request.POST['DOB']
        data.address=request.POST['Address']
        data.email=request.POST['Email']  
        data.username=request.POST['UserName']
        data.save()
        return redirect(pharm_home)
    else:
        return render(request,'pharmacy/edit profilep.html',{'datas':data})
    
    
    
# def pharm_home(request):
# #       return render(request,'pharmacy/homep.html')
#     medicines = medicine.objects.filter(pharmacy_id=request.user)
#     return render(request, 'pharmacy/homep.html', {'medicines': medicines})

def pharm_home(request):
    company= CustomeUser.objects.filter(usertype='company').count()
    Orders = order.objects.all().count()
    # medicines = medicine.objects.filter(pharmacy_id=request.user)
    # return render(request, 'pharmacy/homep.html',{'company':company,'Orders':Orders} )
    return render(request, 'pharmacy/homep.html',{'company':company,'Orders':Orders} )

# 




def add_medicine(request):
    if request.method == 'POST':
        name = request.POST['medicineName']
        price = request.POST['pricePerUnit']
        description = request.POST['description']
        manufacturer = request.POST['manufacturer']
        quantity = request.POST['quantity']
        expiry_date = request.POST['expiryDate']
        brandname=request.POST['brandName']
        genericName=request.POST['genericName']
        strength=request.POST['strength']
        medicine_data = medicine.objects.create( pharmacy_id=request.user,name=name,price=price,strength=strength,brandname=brandname,genericname=genericName,description=description,manufacturer=manufacturer,quantity=quantity,expiry_date=expiry_date)
        medicine_data.save()
        return redirect(pharm_home)
        # return HttpResponse ('medicine_view')
    else:
        return render(request, 'pharmacy/medicine.html')
        # return HttpResponse('sucessfuly')

def edit_medicine(request,id):
    data=medicine.objects.get(id=id)
    if request.method=='POST':
        data.name=request.POST['medicineName']
        data. price = request.POST['pricePerUnit']
        data.description = request.POST['description']
        data.manufacturer = request.POST['manufacturer']
        data.quantity = request.POST['quantity']
        data.expiry_date = request.POST['expiryDate']
        data.brandname=request.POST['brandName']
        data.genericName=request.POST['genericName']
        data.strength=request.POST['strength']
        data.save()
        return redirect(pharm_home)
    else:
        return render(request,'pharmacy/edit_medicine.html',{'datas':data})
def delete_med(request,id):   
    medicines = medicine.objects.get(id=id)
    medicines.delete()
    return redirect(pharm_home)
   
def medicine_view(request,id):
    medicines = medicine.objects.get(id=id)
    return render(request, 'pharmacy/viewmedicine.html',{'medicines': medicines})

def order_product(request):
    pharmacy=CustomeUser.objects.get(id=request.user.id)
    company_order = order.objects.filter(pharmacy_id=pharmacy)
    
# def create_company_order(request):
#     companies = company.objects.all()
#     medicines = medicine.objects.all()
    
#     if request.method == 'POST':
#         company_id = request.POST.get('company')
#         expected_delivery_date = request.POST.get('expected_delivery_date')
#         company =
        
#         order = CompanyOrder.objects.create(
#             company=company,
#             expected_delivery_date=expected_delivery_date,
#             order_date=timezone.now()
#         )
        
#         medicine_ids = request.POST.getlist('medicines')
#         quantities = request.POST.getlist('quantities')
#         unit_prices = request.POST.getlist('unit_prices')
        
#         for i in range(len(medicine_ids)):
#             medicine = get_object_or_404(Medicine, id=medicine_ids[i])
#             quantity = int(quantities[i])
#             unit_price = float(unit_prices[i])
            
#             CompanyOrderItem.objects.create(
#                 order=order,
#                 medicine=medicine,
#                 quantity=quantity,
#                 unit_price=unit_price
#             )
        
#         return redirect('company_order_list')
    
#     return render(request, 'company_orders/create_order.html', {'companies': companies, 'medicines': medicines})


# def pharmacy_vieworder(request):
#     pharmacy_user = CustomeUser.objects.get(id=request.user.id)
#     pharmacy_medicines = medicine.objects.filter(pharmacy_id=pharmacy_user)
#     # Orders = order.objects.filter(medicine_id=pharmacy_medicines)
#     Orders = order.objects.all()
#     return render(request, 'pharmacy/userorder_get.html', {'Orders': Orders, 'pharmacy_user': pharmacy_medicines})
# # 

#######user order#$#####3
def pharmacy_vieworder(request):
    Orders = order.objects.all()
    return render(request,'pharmacy/userorder_get.html',{'Orders': Orders})

def pharmacy_viewcompany(request):
    company= CustomeUser.objects.filter(usertype='company')
    return render(request,'pharmacy/pharm_comany.html',{'company': company})

def pharmacy_userhistory(request):
    user=CustomeUser.objects.get(id=request.user.id)
    history = order.objects.filter(user_id=user)
    history1 = order.objects.all()
    return render(request,'pharmacy/user_history.html',{'history': history,'history1': history1})

def pharmacy_history(request):
    return render(request,'pharmacy/historypage1.html')

#         return redirect(pharm_home)

#*****************delivery**********
def delivery_Register(request):
    if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['Email']
            if CustomeUser.objects.filter(email=email).exists():
             return render(request,'delivery/dlvy_register.html',{'error':'email already exists'})
            address = request.POST['Address']
            phoneno = request.POST['Phonenumber']
            if CustomeUser.objects.filter(phone_number=phoneno).exists():
             return render(request,'delivery/dlvy_register.html',{'error':'username already exists'})
            username = request.POST['UserName']
            if CustomeUser.objects.filter(username=username).exists():
             return render(request,'delivery/dlvy_register.html',{'error':'username already exists'})
            password = request.POST['Password']
            Confirmpassword=request.POST['Confirmpassword']
            if password!=Confirmpassword:
             return render(request,'delivery/dlvy_register.html',{'error':'password not matching'})
            # image=request.FILES['Image']
            License=request.FILES['license']
            data=CustomeUser.objects.create_user(first_name=name,email=email,license=License,address=address,phone_number=phoneno,password=password,username=username,usertype='delivery')
            data.save()
            return render(request,'login.html')
    else:
           return render(request,'delivery/dlvy_register.html')
       
       
def deliver_profile(request):
    data=CustomeUser.objects.get(id=request.user.id)
    return render(request,'delivery/delivery_profile.html',{'data':data})

def deliver_home(request):
    data=order.objects.filter(id=request.user.id).count()
    # pharmacy_user = CustomeUser.objects.get(id=request.user.id)
    # return render(request,'user/delivery_order.html',{'pharmacy_user':pharmacy_user})
    
    return render(request,'delivery/delivery_home.html',{'data':data})

def delivr_order_user(request):
    Orders = order.objects.all()
    return render(request,'delivery/user_order.html',{'Orders': Orders})

#####lst cheyn

# def history(request):
#     return HttpResponse("sucess")
# def delivery_review(request):
#     return HttpResponse("sucess review")

########doctor#######
def doctor_Register(request):
    if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['Email']
            if CustomeUser.objects.filter(email=email).exists():
             return render(request,'doctor/doc_register.html',{'error':'email already exists'})
            address = request.POST['Address']
            phoneno = request.POST['Phonenumber']
            if CustomeUser.objects.filter(phone_number=phoneno).exists():
             return render(request,'doctor/doc_register.html',{'error':'username already exists'})
            username = request.POST['UserName']
            if CustomeUser.objects.filter(username=username).exists():
             return render(request,'doctor/doc_register.html',{'error':'username already exists'})
            password = request.POST['Password']
            Confirmpassword=request.POST['Confirmpassword']
            if password!=Confirmpassword:
             return render(request,'doctor/doc_register.html',{'error':'password not matching'})
            # image=request.FILES['Image']
            Certification=request.FILES['Certification']
            data=CustomeUser.objects.create_user(first_name=name,email=email,certification=Certification,address=address,phone_number=phoneno,password=password,username=username,usertype='doctor')
            data.save()
            return render(request,'login.html')
    else:
           return render(request,'doctor/doc_register.html')
       
def doctor_profile(request):
    user=CustomeUser.objects.get(id=request.user.id)
    return render(request,'doctor/doctor_profilm.html',{'data':user})



def doctor_edit(request):
    data=CustomeUser.objects.get(id=request.user.id)
    if request.method=='POST':
        data.first_name=request.POST['Name']
        data.age=request.POST['age']
        data.phone_number=request.POST['Phonenumber']
        data.dob=request.POST['DOB']
        data.address=request.POST['Address']
        data.email=request.POST['Email']  
        data.username=request.POST['UserName']
        data.save()
        return redirect(pharm_home)
    else:
        return render(request,'doctor/doctor_editprofile.html',{'datas':data})
    
    
    
def doctor_home(request):
    data=order.objects.filter(id=request.user.id)
    # pharmacy_user = CustomeUser.objects.get(id=request.user.id)
    # return render(request,'user/delivery_order.html',{'pharmacy_user':pharmacy_user})
    return render(request,'doctor/doctor_home.html',{'data':data})
    # return render(request, 'doctor/doctor_home.html', {'medicines': medicines})






####admin####
       
def admin(request):
    data = CustomeUser.objects.filter(status="pending")
    print(data)
    return render(request,'admin/admin_status.html',{'data':data})


def admin_status(request,id):
    # data1= CustomeUser.objects.get(id=data.pharmacy_id) 
    data= CustomeUser.objects.get(id=id) 
    if request.method == "POST":
        status=request.POST['status']
        try:
            if status =="accept":
                    data.status = status
                    data.save()
                    return redirect(Login)
                
            elif status =="reject":
                    data.status = status
                    data.save()
                    return redirect(Login)
            else:
                  return HttpResponse("error")
        except Exception as e:
            return HttpResponse({e})
            
    else:
            return redirect(admin)



# def admin(request):
#     # Fetch users with a status of "pending"
#     data = CustomeUser.objects.filter(status="pending")
#     # Render the admin status page with the pending users
#     return render(request, 'admin/admin_status.html', {'data': data})

# def admin_status(request, id):
#     # Fetch the user with the given ID
#     data = CustomeUser.objects.get(id=id)

#     if request.method == "POST":
#         # Get the status from the POST request
#         status = request.POST['status']

#         try:
#             # Check if status is either "accept" or "reject"
#             if status == "accept":
#                 # Update the user's status to "accept"
#                 data.status = status
#                 data.save()
#                 # Redirect to the login view after updating the status
#                 return redirect(Login)
#             elif status == "reject":
#                 # Update the user's status to "reject"
#                 data.status = status
#                 data.save()
#                 # Redirect to the login view after updating the status
#                 return redirect(Login)
#             else:
#                 # Return an error response if the status is invalid
#                 return HttpResponse("error")
#         except Exception as e:
#             # Handle any exceptions and return an error message
#             return HttpResponse({e})
#     else:
#         # Redirect to the admin view if the request method is not POST
#         return redirect(admin)



########company#######
def company_Register(request):
    if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['Email']
            if CustomeUser.objects.filter(email=email).exists():
             return render(request,'company/company_register.html',{'error':'email already exists'})
            address = request.POST['Address']
            phoneno = request.POST['Phonenumber']
            if CustomeUser.objects.filter(phone_number=phoneno).exists():
             return render(request,'company/company_register.html',{'error':'username already exists'})
            username = request.POST['UserName']
            if CustomeUser.objects.filter(username=username).exists():
             return render(request,'company/company_register.html',{'error':'username already exists'})
            password = request.POST['Password']
            Confirmpassword=request.POST['Confirmpassword']
            if password!=Confirmpassword:
             return render(request,'company/company_register.html',{'error':'password not matching'})
            # image=request.FILES['Image']
            Certification=request.FILES['Certification']
            data=CustomeUser.objects.create_user(first_name=name,email=email,certification=Certification,address=address,phone_number=phoneno,password=password,username=username,usertype='company')
            data.save()
            return render(request,'login.html')
    else:
           return render(request,'company/company_register.html')
       
def company_profile(request):
    user=CustomeUser.objects.get(id=request.user.id)
    return render(request,'company/company_profile.html',{'data':user})



def company_edit(request):
    data=CustomeUser.objects.get(id=request.user.id)
    if request.method=='POST':
        data.first_name=request.POST['Name']
        data.phone_number=request.POST['Phonenumber']
        data.address=request.POST['Address']
        data.email=request.POST['Email']  
        data.username=request.POST['UserName']
        data.save()
        return redirect(pharm_home)
    else:
        return render(request,'doctor/doctor_editprofile.html',{'datas':data})
    
    
    
# def company_home(request):
#     data=order.objects.filter(id=request.user.id)
#     # pharmacy_user = CustomeUser.objects.get(id=request.user.id)
#     # return render(request,'user/delivery_order.html',{'pharmacy_user':pharmacy_user})
#     return render(request,'doctor/doctor_home.html',{'data':data})
#     # return render(request, 'doctor/doctor_home.html', {'medicines': medicines})
