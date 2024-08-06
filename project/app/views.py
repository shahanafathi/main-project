from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from .models import CustomeUser,medicine,cart,order,wishlist,Category
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
    if request.method == "POST":
        Username = request.POST['username']
        Password = request.POST['password']
        admin_user = auth.authenticate(request,username=Username,password=Password)
        if admin_user is not None and admin_user.is_staff:
            auth.login(request,admin_user)
            # return redirect('/admin/')  # Redirect to the admin dashboard
            return redirect(admin)
        
        data = auth.authenticate(username=Username,password=Password)
        if data is not None:
            auth.login(request,data)
            if data.usertype == "user" :
             return redirect(user_home)
            if data.usertype == "pharmacy" and data.status == "approved":
                return redirect(pharm_home)
            if data.usertype == "pharmacy" and data.status == "pending":
                return HttpResponse("Can't login without approval of admin.Either wait for 1 day or register again")   
            # elif data.usertype == "deliver" and data.status == "pending":
            #     return HttpResponse("Can't login without approval of admin.Either wait for 1 day or register again")
            # elif data.usertype == "deliver" and data.status == "accept":
            #     return redirect(deliver_profile)
            
            else:
                context ={
                    'message': "Invalid credentials"
                    }
                return render(request, 'login.html', context)

    # Render the login form for GET requests
    else:
      return render(request, 'login.html')


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

def search_medicines(request):
    if request.method=='POST':
        Search=request.POST.get('search','')
        data = medicine.objects.filter(name__icontains=Search)
        return render(request,'user/userhome.html',{'datas': data,'search': Search})
    else:
        # return redirect(user_home)
            return render(request,'user/userhome.html',{'datas': data,'search': Search})
  
  
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
#     datas = CustomeUser.objects.get(id=request.user.id)
#     medicine_item = medicine.objects.get(id=id)
#     cart_items = cart.objects.all()
#     if cart.objects.filter(medicine_id=medicine_item, user_id=datas).exists():
#         return render(request, 'user/cartview.html', {'message': 'This item already exists in your cart', 'cart_items': cart_items})
#     else:
#         cart_add = cart.objects.create(medicine_id=medicine_item, user_id=datas)
#         cart_add.save()
#         return redirect('cart_view') 
    
# def cart_view(request):
#     # cart_items = cart.objects.filter(user_id=request.user.id)
#     cart_items = cart.objects.all()
#     # print(cart_items)
#     return render(request, 'user/cartview.html', {'cart_items': cart_items})

def add_to_cart(request, id):
    user = CustomeUser.objects.get(id=request.user.id)
    medicine_item = medicine.objects.get(id=id)
    cart_items = cart.objects.filter(user_id=user)  # Filter by current user

    # Check if the medicine is already in the cart
    if cart.objects.filter(medicine_id=medicine_item, user_id=user).exists():
        return render(request, 'user/cartview.html', {
            'message': 'This item already exists in your cart',
            'cart_items': cart_items
        })
    else:
        # Add the medicine to the cart
        cart.objects.create(medicine_id=medicine_item, user_id=user)
        return redirect('cart_view')  # Redirect to cart view

def cart_view(request):
    user = request.user
    cart_items = cart.objects.filter(user_id=user)  # Filter cart items by current user
    return render(request, 'user/cartview.html', {'cart_items': cart_items})

def remove_cart(request, id):
    user = request.user
    # Delete the specific cart item for the current user
    cart.objects.filter(id=id, user_id=user).delete()
    return redirect('cart_view')  # Redirect to cart view


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
# def order_item(request):
#     datas=CustomeUser.objects.get(id=request.user.id)
#     cart_item = cart.objects.filter(user_id=datas)
#     var=order.objects.filter(user_id=datas)
#     Ttl_amounts=0
    
#     for item in cart_item:
#         total_amt= item.medicine_id.price*item.medicine_id.quantity
#         Ttl_amounts += total_amt
#         order_item=order.objects.create(user_id=datas,medicine_id=item.medicine_id,total_amount=total_amt, quantity=item.quantity)
#         order_item.save()
#         # return redirect( order_view)
#         return render(request,'user/order.html', {'order_item': cart_item,'total_amounts':Ttl_amounts})


def order_item(request):
    datas=CustomeUser.objects.get(id=request.user.id)
    cart_item = cart.objects.filter(user_id=datas)
    
    
    for item in cart_item:

        order_item=order.objects.create(user_id=datas,medicine_id=item.medicine_id)
        order_item.save()
        cart_item.delete()
        return redirect(cart_view)
#         return render(request,'user/order.html', {'order_item': cart_item,'total_amounts':Ttl_amounts})


def order_view(request):
    datas = CustomeUser.objects.get(id=request.user.id)
    order_items = order.objects.filter(user_id=datas)
    # order_items = order.objects.all()order_items
    # total_amounts = sum(item.total_amount for item in order_items)  # Calculate total for display
    # return render(request, 'user/order1.html', {'order_items': order_items})
    return render(request, 'user/order1.html', {'order_items': order_items})
# 
# def remove_order(request,id):
#     datas = CustomeUser.objects.get(id=request.user.id)

#     order_del = order.objects.get(id=id)
#     order_del.delete()
#     # return redirect( order_item)
#     return render(request,'user/order.html')

# def remove_order(request, order_id):
#     user_data = CustomeUser.objects.get(id=request.user.id)
#     order_item = order.objects.get(id=order_id, user_id=user_data)
#     order_item.delete()
#     return render(request, 'user/order2.html')
    
#        #***********pharmacy**********

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
        data.Phonenumber=request.POST['Phonenumber']
        data.DOB=request.POST['DOB']
        data.Address=request.POST['Address']
        data.email=request.POST['Email']  
        data.username=request.POST['UserName']
        data.save()
        return redirect(pharm_home)
    else:
        return render(request,'pharmacy/edit profilep.html',{'datas':data})
    
    
    
def pharm_home(request):
#       return render(request,'pharmacy/homep.html')
    medicines = medicine.objects.filter(pharmacy_id=request.user)
    return render(request, 'pharmacy/homep.html', {'medicines': medicines})

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

def pharmacy_vieworder(request):
    pharmacy_user = CustomeUser.objects.get(id=request.user.id)
    pharmacy_medicines = medicine.objects.filter(pharmacy_id=pharmacy_user)
    orders = order.objects.filter(medicine_id__in=pharmacy_medicines)
    return render(request, 'pharmacy/userorder_get.html', {'orders': orders, 'pharmacy_user': pharmacy_user})
# 

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