from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from .models import CustomeUser,medicine,cart,order,wishlist
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
        
        if user is not None:
            login(request, user)
            if user.is_staff:
                return redirect('/admin/')  # Redirect to the admin dashboard
            else:
                if user.usertype == "user":
                    return redirect(user_home)  # Redirect to the user profile
                elif user.usertype == "pharmacy":
                    return redirect(pharm_home)# Redirect to the pharmacy profile
                elif user.usertype == "delivery":
                    # return HttpResponse('sucess')
                    return redirect(deliver_profile)
                # elif user.usertype == "admin":
                #     return redirect('/admin/')  # Redirect to the admin dashboard
                else:
                    return HttpResponse("error")
        else:
            context = {
                'message': "Invalid credentials"
            }
            return render(request, 'login.html', context)
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
# def add_to_cart(request,id):
#     datas=CustomeUser.objects.get(id=request.user.id)
#     # print(datas)
#     medicine_item = medicine.objects.get(id=id)
#     cart_items = cart.objects.all()
  
    
#     if cart.objects.filter(medicine_id=medicine_item,user_id=datas).exists():
#              return render(request,'user/user_home.html',{'message':'already exists in the cart','cart_items': cart_items})
#     else:
#                 cart_add=cart.objects.create(medicine_id=medicine_item,user_id=datas)
#                 cart_add.save()
#                 return redirect(cart_view)
        # return render(request, 'user/cartview.html',{'item':medicine_item,'datas':datas})
        # return HttpResponse('sucess')
    # else:
    #     return render(request, 'user/cart.html',{'item':medicine_item,'datas':datas})

# def add_to_cart(request,id):
#     datas=CustomeUser.objects.get(id=request.user.id)
#     medicine_item = medicine.objects.get(id=id)
#     if cart.objects.filter(medicine_id=medicine_item,user_id=datas).exists():
#             return render(request,'user/user_home.html',{'message':'already exists in the cart','cart_items': cart_items})
#     else:
#         cart_add=cart.objects.create(medicine_id=medicine_item,user_id=datas)
#         cart_add.save()
        
#         return render(request, 'user/cart1.html',{'item':cart_add,'datas':datas})
    

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
    var=order.objects.filter(user_id=datas)
    Ttl_amounts=0
    
    for item in cart_item:
        total_amt= item.medicine_id.price*item.medicine_id.quantity
        Ttl_amounts += total_amt
        order_item=order.objects.create(user_id=datas,medicine_id=item.medicine_id,total_amount=total_amt, quantity=item.quantity)
        order_item.save()
        # return redirect( order_view)
        return render(request,'user/order.html', {'order_item': cart_item,'total_amounts':Ttl_amounts})


def order_view(request):
    datas = CustomeUser.objects.get(id=request.user.id)
    order_items = order.objects.filter(user_id=datas)
    # total_amounts = sum(item.total_amount for item in order_items)  # Calculate total for display
    return render(request, 'user/order.html', {'order_items': order_items})
    # return render(request, 'user/order.html', {'order_items': order_items})
# 
def remove_order(request,id):
    datas = CustomeUser.objects.get(id=request.user.id)

    order_del = order.objects.get(id=id)
    order_del.delete()
    # return redirect( order_item)
    return render(request,'user/order.html')

# def remove_order(request, order_id):
#     user_data = CustomeUser.objects.get(id=request.user.id)
#     order_item = order.objects.get(id=order_id, user_id=user_data)
#     order_item.delete()
#     return render(request, 'user/order2.html')
    
#        #***********pharmacy**********
       
       
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
# # def search_medicine(request):
#     if request.method=='POST':
#         Search=request.POST['search']
#         user = medicine.objects.filter(usertype='pharmacy',name__icontains=Search)
#         return render(request,'pharmacy/homep.html',{'users': user})
#     else:
#         return redirect(pharm_home)

def update_order_status(request, order_id):
    if request.method == 'POST':
        try:
            order = order.objects.get(id=order_id)
            new_status = request.POST.get('status')
            order.status = new_status
            order.save()
            messages.success(request, f"Order {order_id} status updated to {new_status}.")
        except order.DoesNotExist:
            messages.error(request, "Order not found.")
    
    return redirect('pharmacy_orders')

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
       