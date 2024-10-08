from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from .models import CustomeUser,medicine,cart,order,wishlist,Category,prescription,CompanyOrder
# from django.shortcuts import get


from django.urls import reverse
from django.contrib import messages

# Create your views here.

def index(request):
     return redirect(home)
def home(request):
      return render(request,'home.html')
# ***************main login****** 

# def Login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         #  Authenticate superusers (admins)
#         print(user)
         
#         admin_user = authenticate(request, username=username, password=password)
#         if admin_user is not None and admin_user.is_staff:
#             login(request,admin_user)
#             #  Authenticate superusers (admins)
#             # return redirect(admin_profile)  # Redirect to the admin dashboard
#         elif user is not None:
#             # If not an admin, check regular users
#             login(request, user)
#             if user.usertype == "user":     #user profile
#                 return redirect(user_home)
#             elif user.usertype == "pharmacy":
#                 return redirect(pharm_home)
#             elif user.usertype == "delivery":
#                 return redirect(deliver_home)
#             elif user.usertype == "doctor":
#                 return redirect(doctor_profile)
#             elif user.usertype == "company":
#                 return redirect(company_profile)
#             elif user.usertype=="admin":
#                 # return HttpResponse('homepage sucess')
#                   return redirect('/admin/')
#             return render(request, 'login.html', context)
#         else:
#             context = {
#                 'message': "Invalid credentials"
#             }
#             return render(request, 'login.html', context)
#     else:
#         return render(request, 'login.html')
    


def Login(request):
    if request.method == "POST":
        Username = request.POST['username']
        Password = request.POST['password']
        admin_user = auth.authenticate(request,username=Username,password=Password)
        if admin_user is not None and admin_user.is_staff:
            auth.login(request,admin_user)
            return redirect('/admin/')  
            # return redirect(admin)
        
        data = auth.authenticate(username=Username,password=Password)
        if data is not None:
            auth.login(request,data)
            if data.usertype == "user" :
             return redirect(user_home)
         
            elif data.usertype == "pharmacy":
                return redirect(pharm_home)
            
            # if data.usertype == "pharmacy" and data.status == "approved":
            #     return redirect(pharm_home)
            
            # if data.usertype == "pharmacy" and data.status == "pending":
            #     return HttpResponse("Can't login without approval of admin.Either wait for 1 day or register again")   
            
            if data.usertype == "company" and data.status == "approved":
                return redirect(company_home)
            
            if data.usertype == "company" and data.status == "pending":
                 return HttpResponse("Can't login without approval of admin.Either wait for 1 day or register again")
            # elif data.usertype == "deliver" and data.status == "accept":
            #     return redirect(deliver_profile)
            
            else:
                context ={
                    'message': "Invalid credentials"
                    }
                return render(request, 'login.html', context)

    #
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
            Image=request.FILES['Image']
            print("image :   ",Image)
            data=CustomeUser.objects.create_user(first_name=name,Image=Image,email=email,address=address,age=age,phone_number=phoneno,dob=DOB,password=password,username=username,usertype='user')
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
        data.phone_number=request.POST['Phonenumber']
        data.dob=request.POST['DOB']
        data.address=request.POST['Address']
        data.email=request.POST['Email']  
        data.username=request.POST['UserName']
        if 'Image' in request.FILES:
            data.Image = request.FILES['Image']
        data.save()
        return redirect(userprofile)
    else:
        return render(request,'user/editprofile.html',{'datas':data})
       
##################################


def user_home(request):
    medicines = medicine.objects.all()
    # reviews = order.objects.all()
    pharmacies = CustomeUser.objects.filter(usertype="pharmacy")
    category = Category.objects.all()
    return render(request, 'user/userhome.html', {'medicines': medicines,'catogary':category,'pharmacies':pharmacies})


    
    
# def search_phrmplace(request):
#     if request.method == 'POST':
#         # search_query = request.POST.get('search', '')
#         search_query = request.POST.get('search')
#         pharmarcy= CustomeUser.objects.filter(address__icontains=search_query,usertype="pharmacy")
#         return render(request, 'user/userhome.html', {'pharmarcy': pharmarcy,'search_query': search_query})
#     else: 

#         return render(request, 'user/userhome.html', {'pharmarcy':CustomeUser.objects.all()})
    

def search_phrmplace(request):
    if request.method == 'POST':
        # search_query = request.POST.get('search', '')
        search_query = request.POST.get('search')
        pharmarcy= CustomeUser.objects.filter(address__icontains=search_query,usertype="pharmacy")
        return render(request, 'user/userhome.html', {'pharmarcy': pharmarcy,'search_query': search_query})
    else: 
          pharmacies = CustomeUser.objects.filter(usertype="pharmacy")
          return render(request, 'user/userhome.html', {'pharmarcy':CustomeUser.objects.all(),'pharmarcy':pharmacies})
    
    
    
    
# def search_phrmplace(request):
#     if request.method == 'POST':
#         search_query = request.POST.get('search', '')  # Default to empty string if no search query
#         pharmacies = CustomeUser.objects.filter(address__icontains=search_query, usertype="pharmacy")
#         return render(request, 'user/userhome.html', {'pharmarcy': pharmacies, 'search_query': search_query})
#     else: 
#         pharmacies = CustomeUser.objects.filter(usertype="pharmacy")  # Fetch all pharmacies for GET request
#         return render(request, 'user/userhome.html', {'pharmarcy': pharmacies})

    
#######################EACH PHARMACY >>CLICK ON VIEW>>>VIEW --MEDICINE I IT   that page #######

def category_dropdown(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        category_select = request.POST.get('category')
        print(category_select)
        medicines = medicine.objects.filter(category_name=category_select)
        return render(request, 'user/medicine_pharmacy.html', {'medicines': medicines, 'category_select': category_select,'categories':categories})
        
    else: 
        return render(request, 'user/medicine_pharmacy.html', {'medicines': medicine.objects.all()})
    


def search_medicines(request,id):
    pharmacy=CustomeUser.objects.get(id=id)
    if request.method == 'POST':
        search_query = request.POST.get('search', '')
        medicines = medicine.objects.filter(name__icontains=search_query,pharmacy_id=pharmacy)
        context = {'medicines': medicines,
                   'search_query': search_query,
                   'pharmacy':pharmacy}
        return render(request, 'user/medicine_pharmacy.html', context)
    else: 
        return render(request, 'user/medicine_pharmacy.html', {'medicines': medicine.objects.all()})
  
def medicine_view(request,id):
    # medicines = medicine.objects.get()
    medicine1 = medicine.objects.get(id=id)
    return render(request, 'user/medicinuser_view.html',{'medicine': medicine1})

def user_medicine(request,id):
    medicines = medicine.objects.filter(pharmacy_id=id)
    pharmacy = CustomeUser.objects.get(id=id)
    return render(request, 'user/medicine_pharmacy.html', {'medicines': medicines,'pharmacy':pharmacy})

# def usermedicine_view(request):
#     medicines = medicine.objects.all()
#     return render(request, 'pharmacy/viewmedicine.html',{'medicines': medicines})


def upload_prescription(request,id):
    data=CustomeUser.objects.get(id=request.user.id)
    pharmacy=CustomeUser.objects.get(id=id)
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        address = request.POST.get('address')
        prescription_file=request.FILES['prescription_file']
        prescriptions=prescription.objects.create(user_id=data,name=name,age=age,
                                                  prescription_file=prescription_file,
                                                  address=address,
                                                  pharmancy_id=pharmacy,
                                                  )
        prescriptions.save()
        # return redirect('user/prescription_success')
        # return HttpResponse('success')
        return render(request, 'user/prescription_success.html',{'data':data,'pharmacy':pharmacy,'prescriptions':prescriptions})
        

        
    else:
        return render(request, 'user/upload_prescription.html',{'data':data,'pharmacy':pharmacy})




def help_page(request):
    return render(request, 'user/help.html')
# def user_pharmacy_upload(request,id):
#     user= CustomeUser.objects.get(id=request.user.id)
#     # pharmacy=CustomeUser.objects.get(id=id)
#     return render(request, 'user/medicinepharmacy.html',{'user':user})




#########  user cart#######
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
    user =CustomeUser.objects.get(id=request.user.id)
    cart_items = cart.objects.filter(user_id=user)  # Filter cart items by current user
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
    
    # return render(request, 'user/wishlist1.html', {'item': medicine_item, 'datas': datas,'item':wishlist_add})


def wishlist_view(request):
    wishlist_items = wishlist.objects.filter(user_id=request.user.id)
    # wishlist_items = wishlist.objects.all()

    return render(request,'user/wishlist1.html', {'wishlist': wishlist_items})

def remove_wishlist(request,id):
    wishlist_del = wishlist.objects.get(id=id)
    wishlist_del.delete()
    return redirect( wishlist_view)

######## order list####
def order_item(request):
    datas = CustomeUser.objects.get(id=request.user.id)
    cart_items = cart.objects.filter(user_id=datas)
    Ttl_amounts = 0

    if request.method == 'POST':
        for item in cart_items:
            # Retrieve the selected quantity from the POST request
            quantity_key = f'quantity_{item.id}'
            selected_quantity_str = request.POST.get(quantity_key)

            # Check if the quantity is provided and valid
            if selected_quantity_str and selected_quantity_str.isdigit():
                selected_quantity = int(selected_quantity_str)
            else:
                selected_quantity = 1  # Assign a default value if not provided or invalid

            # Update the item quantity with the selected quantity
            item.quantity = selected_quantity
            item.save()

            # Calculate the total amount for the selected quantity
            total_amt = item.medicine_id.price * selected_quantity
            Ttl_amounts += total_amt

        # Creating the order
            order_item = order.objects.create(
                user_id=datas,
                medicine_id=item.medicine_id,
                total_amount=Ttl_amounts,
                quantity=selected_quantity  
            )
            order_item.save()

        return render(request, 'user/order.html', {'order_item': cart_items, 'total_amounts': Ttl_amounts})

    return render(request, 'user/order.html', {'order_item': cart_items, 'total_amounts': Ttl_amounts})


# ########################

# def payment_page(request):
#     # Retrieve the current user
#     user = CustomeUser.objects.get(id=request.user.id)
    
#     # Get the cart items for the user
#     cart_items = cart.objects.filter(user_id=user)
    
#     # Initialize total amounts
#     Ttl_amounts = 0

#     # Iterate over the cart items to calculate the total price
#     for item in cart_items:
#         # Retrieve the quantity from the POST request (if provided)
#         quantity_key = f'quantity_{item.id}'
#         selected_quantity_str = request.POST.get(quantity_key)
        
#         # Validate the quantity, if not provided or invalid, set default to 1
#         if selected_quantity_str and selected_quantity_str.isdigit():
#             selected_quantity = int(selected_quantity_str)
#         else:
#             selected_quantity = 1  # Default value if not provided

#         # Calculate the total amount for this item
#         total_amt = item.medicine_id.price * selected_quantity
#         Ttl_amounts += total_amt  # Accumulate the total amounts

#     # Render the template with the updated cart items and total price
#     return render(request, 'user/payment1.html', {'cart_items': cart_items,'total_price': Ttl_amounts,})


def payment_page(request):
    # user = request.user
    user = CustomeUser.objects.get(id=request.user.id)
    order_item= cart.objects.filter(user_id=user)
    Ttl_amounts=0
   
    # total=order.objects.filter()
    for item in order_item:
        
        total_amt=(item.medicine_id.price*item.medicine_id.quantity)
        print(total_amt)
        Ttl_amounts += total_amt
        # order_item=order.objects.create(user_id=user,medicine_id=item.medicine_id,total_amount=total_amt, quantity=item.quantity)
        # order_item.save()
        # total_prices = item.medicine_id.price * item.medicine_id.quantity 
        return render(request, 'user/payment1.html', {'order_item': order_item,'total_price':Ttl_amounts,'total':total_amt})
def process_payment(request):
    if request.method == 'POST':
        
        cardholder_name = request.POST.get('cardholder_name')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
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
    # for item in order_items:
    # total_amounts = order_items.total_amount  # Calculate total for display
    # return render(request, 'user/.html', {'order_items': order_items})
    return render(request, 'user/order_view.html', {'order_items': order_items})

def remove_orderview(request,id):
   
    order_del =  order.objects.get(id=id)
    order_del.delete()
    return redirect(order_view)

def pharmacy_user(request,id):
    user= CustomeUser.objects.get(id=request.user.id)
    pharmacy=CustomeUser.objects.get(id=id)
    

####debitt card system######
def Debitcard(request):
    if request.method == 'POST':
        cardholder_name = request.POST.get('cardholder_name')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        return redirect('order_confirmation')
    
    else:
        return render(request, 'user/Debit_card.html')

def cash_on_delivery(request):
    user = CustomeUser.objects.get(id=request.user.id)
    cart_items = cart.objects.filter(user_id=user)
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address')

        if not delivery_address:
            messages.error(request, "Please provide a delivery address.")
            return redirect('cash_on_delivery')

        for item in cart_items:
            order_item = order.objects.create(
                user_id=user, 
                medicine_id=item.medicine_id,
                total_amount=item.medicine_id.price * item.quantity,
                quantity=item.quantity,
                delivery_address=delivery_address,
                status='PENDING',  
                payment_status='PENDING'
            )
            order_item.save()

        cart_items.delete()  
        return redirect('order_confirmation1')

    return render(request, 'user/cash_on_delivery.html', {'cart_items': cart_items})







#   #***********pharmacy**********

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
            Image=request.FILES['Image']
            print(Image)
            data=CustomeUser.objects.create_user(first_name=name,email=email,Image=Image,address=address,phone_number=phoneno,password=password,username=username,usertype='pharmacy')
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
        data.phone_number=request.POST['Phonenumber']
        data.address=request.POST['Address']
        data.email=request.POST['Email']  
        data.username=request.POST['UserName']
        if 'Image' in request.FILES:
            data.Image = request.FILES['Image']
    
        data.save()
        return redirect(pharm_home)
    else:
        return render(request,'pharmacy/edit_profilep.html',{'datas':data})
    
def pharm_home(request):
    company= CustomeUser.objects.filter(usertype='company').count()
    Orders = order.objects.all().count()
    medicines = medicine.objects.all().count()
    # return render(request, 'pharmacy/homep.html',{'company':company,'Orders':Orders} )
    return render(request, 'pharmacy/homep.html',{'company':company,'Orders':Orders,'medicines':medicines} )



def add_medicine(request):
    data =CustomeUser.objects.get(id=request.user.id)
    datas = Category.objects.all()
    if request.method == 'POST':
        name = request.POST['medicineName']
        price = request.POST['pricePerUnit']
        description = request.POST['description']
        manufacturer = request.POST['manufacturer']
        category = request.POST['category']
        categoryid = Category.objects.get(id=category)
        quantity = request.POST['quantity']
        expiry_date = request.POST['expiryDate']
        strength=request.POST['strength']
        Image=request.FILES['Image']
        medicine_data = medicine.objects.create( pharmacy_id=data,name=name,Image=Image,price=price,strength=strength,description=description,manufacturer=manufacturer,quantity=quantity,category_name=categoryid.category_name,expiry_date=expiry_date)
        medicine_data.save()
        return redirect(pharm_home)
        # return HttpResponse ('medicine_view')
    else:
        return render(request, 'pharmacy/medicine.html',{'datas': datas})
        # return HttpResponse('sucessfuly')
# def catgry(request,id):
#     data=medicine.objects.filter(category_name=id)
#     return render(request, 'pharmacy/view_medicine.html',{'data': data})
        


def edit_medicine(request,id):
    data=medicine.objects.get(id=id)
    if request.method=='POST':
        data.name=request.POST['medicineName']
        data. price = request.POST['pricePerUnit']
        data.description = request.POST['description']
        data.manufacturer = request.POST['manufacturer']
        data.quantity = request.POST['quantity']
        data.expiry_date = request.POST['expiryDate']
        data.strength=request.POST['strength']
        if 'Image' in request.FILES:
            data.Image = request.FILES['Image']
        data.save()
        return redirect(pharm_home)
    else:
        return render(request,'pharmacy/edit_medicine.html',{'datas':data})
    
    
def delete_med(request,id):   
    medicines = medicine.objects.get(id=id)
    medicines.delete()
    return redirect(medicine_viewss)
   
   
   
def medicine_viewss(request,id):
    medicines = medicine.objects.get(id=id)
    print("image : ",medicines.Image)
    return render(request, 'pharmacy/viewmedicine.html',{'medicines': medicines})

def medicine_viewpharma(request):
    medicines = medicine.objects.filter(pharmacy_id=request.user.id)
    return render(request, 'pharmacy/med1.html',{'medicines': medicines})

# def search_catagery(request):
#     if request.method == 'POST':
#         search_query = request.POST.get('search', '')
#         medicines = medicine.objects.filter(name__icontains=search_query)
#         return render(request, 'user/userhome.html', {'medicines': medicines, 'search_query': search_query})
#     else: 
#         return render(request, 'user/userhome.html', {'medicines': medicine.objects.all()})
  
########user>>>order all>>pharmacy seen ########

def pharmacy_vieworder(request):
    pharmacy_user = CustomeUser.objects.get(id=request.user.id)
    pharmacy_medicines = medicine.objects.filter(pharmacy_id=pharmacy_user)
    # Orders = order.objects.filter(medicine_id=pharmacy_medicines)
    Orders = order.objects.all()
    return render(request, 'pharmacy/userorder_get.html', {'Orders': Orders, 'pharmacy_user': pharmacy_medicines})

def userorder_view(request,id):
    data =  order.objects.filter(id=id)
    medicine_list = []
    for i in data:
        medicine_list.append(i.medicine_id)
    return render(request,'pharmacy/viewone_order.html',{'data':data,'medicine_list':medicine_list})
def pharmacy_userhistory(request):
    #  data1=CustomeUser.objects.get(user_id=request.user.id)
     data=order.objects.all()
#     data= order.objects.all()
     return render (request,'pharmacy/user_history.html',{'data':data})
# def pharmacy_history(request):
#     data1=CustomeUser.objects.get(user_id=request.user.id)
#     data= order.objects.all()
#     return render (request,)

def pharmacy_history(request):
    return render(request,'pharmacy/historypage1.html')

def pharmacy_prescription(request):
    prescp=prescription.objects.all()
    return render(request,'')
    
# def stock(request):
#     pharmacy_user = CustomeUser.objects.get(id=request.user.id)
#     pharmacy_medicines = medicine.objects.filter(pharmacy_id=pharmacy_user)
#     data=Category.objects.all()
#     return render(request, 'pharmacy/stock_check.html', {'pharmacy_user': pharmacy_medicines,'data':data})

# def search_medicines(request):
#     if request.method == 'POST':
#         search_query = request.POST.get('search', '')
#         medicines = medicine.objects.filter(name__icontains=search_query)
#         return render(request, 'pharmacy/.html', {'medicines': medicines, 'search_query': search_query})
#     else: 
#         return render(request, 'user/userhome.html', {'medicines': medicine.objects.all()})





#######user order#$#####3

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

####admin####
       
def admin(request):
    data = CustomeUser.objects.filter(status="pending")
    print(data)
    return render(request,'admin/admin_home.html',{'data':data})


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
#     data=CustomeUser.objects.filter(id=request.user.id)
#     # pharmacy_user = CustomeUser.objects.get(id=request.user.id)
#     # return render(request,'user/delivery_order.html',{'pharmacy_user':pharmacy_user})
#     return render(request,'doctor/doctor_home.html',{'data':data})
#     # return render(request, 'doctor/doctor_home.html', {'medicines': medicines})


def company_home(request):
    # Retrieve the current logged-in user
    company_user = CustomeUser.objects.get(id=request.user.id)
    
    # Render the doctor_home.html template with user data
    return render(request, 'company/company_home.html', {'company_user': company_user})

