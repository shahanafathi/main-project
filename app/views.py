from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from .models import CustomeUser,medicine,cart,order,wishlist,Category,prescription,company_order,Delivary,order_delivery,product,ContactUs
# from django.shortcuts import get
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
# Create your views here.

def index(request):
     return redirect(home)
def home(request):
      return render(request,'home1.html')
# ***************main login****** 
def Login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        #  Authenticate superusers (admins)      
        if user is not None:
            # If not an admin, check regular users
            login(request, user)
            if user.usertype == "user":     #user profile
                return redirect(user_home)
            elif user.usertype == "pharmacy":
                return redirect(pharm_home)
            elif user.usertype == "delivery":
                return redirect(deliver_home)
            elif user.usertype == "company":
                return redirect(company_home)
            elif user.usertype=="admin":
                return redirect(admin_home)
                #   return redirect('/admin/')
            return render(request, 'login.html', context)
        else:
            context = {
                'message': "Invalid credentials"
            }
            return render(request, 'login.html', context)
    else:
        return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect(Login)

def about_us(request):
    return render(request,'About_us.html')
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
            data=CustomeUser.objects.create_user(first_name=name,Image=Image,delivery_address=address,email=email,address=address,age=age,phone_number=phoneno,dob=DOB,password=password,username=username,usertype='user')
            data.save()
            # return HttpResponse('sucess')
            return render(request,'login.html')
        else:
            return render(request,'user/register.html')

def userprofile(request):
    if request.user.id:
        users=CustomeUser.objects.get(id=request.user.id)
        return render(request,'user/profile.html',{'data':users})
    else:
        return redirect(Login)
    
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
        
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import PasswordResetRequestForm

# Store OTP temporarily (in a real application, consider using a more secure method)
otp_store = {}

def send_otp(email):
    otp = random.randint(100000, 999999)  # Generate a random 6-digit OTP
    send_mail(
        'Your OTP Code',
        f'Your OTP code is: {otp}',
        'shahanafathima2985@gmail.com',
        [email],
        fail_silently=False,
    )
    return otp

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = CustomeUser.objects.get(email=email)
                otp = send_otp(email) 
                
                context = {
                            "email":email,
                            "otp":otp
                }
                    
                return render(request,'verify_otp.html',context) 
            except User.DoesNotExist:
                messages.error(request, "Email address not found.")
    else:
        form = PasswordResetRequestForm()
    return render(request, 'password_reset_request.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        otpold = request.POST.get('otpold')
        otp = request.POST.get('otp')
        
        if otpold==otp :
            
            context = {
                'otp' : otp,
                'email' : email
            }
            
            return render(request,'set_new_password.html',context)  
        else:
            messages.error(request, "Invalid OTP.")
    return render(request, 'verify_otp.html')

def set_new_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        try:
            user = CustomeUser.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, "Password has been reset successfully.")
            return redirect(Login)  # Redirect to login page
        except User.DoesNotExist:
            messages.error(request, "Email address not found.")
    return render(request, 'set_new_password.html', {'email': email})
    
   ########################
@login_required(login_url='Login')
def user_home(request):
    try:
        if request.user.id:
            medicines = medicine.objects.all()
            wish_list_ids = wishlist.objects.filter(user_id=request.user.id).values_list('medicine_id', flat=True)    
            pharmacies = CustomeUser.objects.filter(usertype="pharmacy")
            category = Category.objects.all()
            context = {
                'medicines': medicines,
                'catogary':category,
                'pharmacies':pharmacies,
                'wish_list_ids':wish_list_ids,
            }
            return render(request, 'user/userhome.html',context)
        else:
            return redirect(Login)
    except CustomeUser.DoesNotExist:
        return redirect(Login)


def medicine_view(request,id):
    medicine1 = medicine.objects.get(id=id)
    return render(request,'user/medicin_view_medproduct.html',{'medicine': medicine1})
  
#######################EACH PHARMACY >>CLICK ON VIEW>>>VIEW --MEDICINE I IT   that page #######

def category_dropdown(request):
    catogory = Category.objects.all()
    if request.method == 'POST':  
        category_select = request.POST.get('category')
        medicines = medicine.objects.filter(category_name=category_select)
        context = {
            'medicines': medicines, 
            'catogory':catogory,      
        }
        return render(request, 'user/userhome.html', context)
        
    else: 
        return render(request, 'user/userhome.html', {'medicines': medicine.objects.all()})

def search_medicines(request):
    # pharmacy=CustomeUser.objects.get(id=id)
    if request.method == 'POST':  
        search_query = request.POST.get('search', '')
        medicines = medicine.objects.filter(name__icontains=search_query)
        catogory1 =Category.objects.all()
        context = {'medicines': medicines,
                   'search_query': search_query,
                   'catogory':catogory1,
                  }
        return render(request, 'user/userhome.html', context)
    else: 
        return render(request, 'user/userhome.html', {'medicines': medicine.objects.all()})
 
@login_required(login_url='Login')
def user_medicine(request,id):
    try:
        medicines = medicine.objects.filter(pharmacy_id=id)
        pharmacy = CustomeUser.objects.get(id=id)
        catogory1 =Category.objects.all()
        for i in medicines:
            
            print(i.Image)
        context={
            'medicines': medicines,
            'pharmacy':pharmacy,
            'catogory':catogory1
            }
        return render(request, 'user/medicine_pharmacy.html',context)
    except CustomeUser.DoesNotExist:
        return redirect(Login)

# def help_page(request):
#     if request.method=='POST':
#         name = request.POST['name']
#         email = request.POST['email']
#         message= request.POST['message']
#         # print(name,email,message)
#         try:
#             datas=ContactUs.objects.create_user()
#             datas.save()
#             # print(email)
#             messages.success(request, " message send sucessfully.")
#             return render(request,'user/help.html',{'datas':datas})
#             # return HttpResponse('sucess')
#         except Exception as e:
          
#             # messages.error(request, "Email address not found.")
#             return render(request,'user/help.html',{'error':e})
#             # return HttpResponse('fail')
#     else:
#        return render(request,'user/help.html')


from django.contrib import messages
from django.shortcuts import render
from .models import ContactUs  # Ensure ContactUs is properly imported
@login_required(login_url='Login')
def help_page(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            message = request.POST.get('message')

            if not name or not email or not message:
                messages.error(request, "All fields are required.")
                return render(request, 'user/help.html')

            try:
                # Save data to the database
                contact_data = ContactUs.objects.create(name=name, email=email, message=message)
                contact_data.save()

                messages.success(request, "Message sent successfully.")
                return render(request, 'user/help.html')
            except Exception as e:
                # Log the exception for debugging purposes if needed
                print(f"Error: {e}")
                messages.error(request, "An error occurred while sending your message.")
                return render(request, 'user/help.html')
        else:
            return render(request, 'user/help.html')
    except CustomeUser.DoesNotExist:
        return redirect(Login)
@login_required(login_url='Login')
def health_blog(request):
    try:
        return render(request,'user/health_blog.html')
    except CustomeUser.DoesNotExist:
        return redirect(Login)

def MEDICINE(request):
    medicines = medicine.objects.all()
    wish_list_ids = wishlist.objects.filter(user_id=request.user.id).values_list('medicine_id', flat=True)
    
    items_per_page = 12
    paginator = Paginator(medicines, items_per_page)
    page = request.GET.get('page', 1)

    try:
        medicines = paginator.page(page)
    except PageNotAnInteger:
       
        medicines = paginator.page(1)
    except EmptyPage:

        medicines = paginator.page(paginator.num_pages)
    context={
        
       'medicines':medicines,
       'wish_list_ids':wish_list_ids,
    }
    return render(request,'user/medicine_pharmacy.html',context)

def add_to_wishlist1(request, id):
    datas = CustomeUser.objects.get(id=request.user.id)
    print(datas)
    medicine_item = medicine.objects.get(id=id)
    wishlist_add = wishlist.objects.create(medicine_id=medicine_item,user_id=datas)
    wishlist_add.save()
    return redirect(MEDICINE)

def remove_to_wishlist1(request,id):
    datas = CustomeUser.objects.get(id=request.user.id)
    medicine_item = medicine.objects.get(id=id)
    rem = wishlist.objects.filter(medicine_id=medicine_item)
    rem.delete()
    return redirect(MEDICINE)

def search_medicines_scnd(request):
    # pharmacy=CustomeUser.objects.get(id=id)
    if request.method == 'POST':
      
        search_query = request.POST.get('search', '')
        medicines = medicine.objects.filter(name__icontains=search_query)
        catogory1 =Category.objects.all()
        context = {'medicines': medicines,
                   'search_query': search_query,
                   'catogory':catogory1,
                  }
        return render(request, 'user/medicine_pharmacy.html', context)
    else: 
        return render(request, 'user/medicine_pharmacy.html', {'medicines': medicine.objects.all()})
 
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
    
# def cart_view(request):
#     user =CustomeUser.objects.get(id=request.user.id)
#     # cart_items = cart.objects.all().count()
#     wishlists=wishlist.objects.filter(user_id=user)
#     for i in wishlists:
#         print(i)
#     cart_items = cart.objects.filter(user_id=user)
#     return render(request, 'user/cartview.html', {'cart_items': cart_items,'wishlists':wishlists})

def cart_view(request):
    user =CustomeUser.objects.get(id=request.user.id)
    cart_items = cart.objects.filter(user_id=user)
    
    if request.method == 'POST':
        for item in cart_items:
            quantity_key = f'quantity_{item.id}'
            if quantity_key in request.POST:
                try:
                    new_quantity = int(request.POST[quantity_key])
                    if new_quantity > 0:
                        item.quantity = new_quantity
                        item.save()
                except ValueError:
                    pass  # Handle invalid input gracefully
    wishlists=wishlist.objects.filter(user_id=user)
    for i in wishlists:
        print(i)
    cart_items = cart.objects.filter(user_id=user)
    return render(request, 'user/cartview.html', {'cart_items': cart_items,'wishlists':wishlists})

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
    return redirect(user_home)

def remove_to_wishlist(request,id):
    datas = CustomeUser.objects.get(id=request.user.id)
    medicine_item = medicine.objects.get(id=id)
    rem = wishlist.objects.filter(medicine_id=medicine_item)
    rem.delete()
    return redirect(user_home)
    
def wishlist_view(request):
    wishlist_items = wishlist.objects.filter(user_id=request.user.id)
    # wishlist_items = wishlist.objects.all()

    return render(request,'user/wishlist1.html', {'wishlist': wishlist_items})

def remove_wishlist(request,id):
    wishlist_del = wishlist.objects.get(id=id)
    wishlist_del.delete()
    return redirect( wishlist_view)

# wishlist to cart in same page:
def wishlist_to_cart(request,id):
    datas = CustomeUser.objects.get(id=request.user.id)
    medicine_item = medicine.objects.get(id=id)
    cart_items = cart.objects.all()
    if cart.objects.filter(medicine_id=medicine_item, user_id=datas).exists():
            return render(request, 'user/cartview.html', {'message': 'This item already exists in your cart', 'cart_items': cart_items})
    else:
            cart_add = cart.objects.create(medicine_id=medicine_item, user_id=datas)
            cart_add.save()
            return redirect(cart_view)
        
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
            # order_item = order.objects.create(
            #     user_id=datas,
            #     medicine_id=item.medicine_id,
            #     total_amount=Ttl_amounts,
            #     quantity=selected_quantity  
            # )
            # order_item.save()

        return render(request, 'user/order.html', {'order_item': cart_items, 'total_amounts': Ttl_amounts,'datas':datas})

    return render(request, 'user/order.html', {'order_item': cart_items, 'total_amounts': Ttl_amounts,'datas':datas})

def delivery_address(request):
    data=CustomeUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address')
        data.delivery_address=delivery_address
        data.save()
        print(data.delivery_address)
        return redirect(order_item)
    else:
        return render(request,'user/delivery_address.html')

        
def payment_page(request):
    # user = request.user
    user = CustomeUser.objects.get(id=request.user.id)
    order_item= cart.objects.filter(user_id=user)
    Ttl_amounts=0
   
    # total=order.objects.filter()
    for item in order_item:
     
        total_amt=(item.medicine_id.price*item.quantity)
        Ttl_amounts+=total_amt
       
        
        # order_item=order.objects.create(user_id=user,medicine_id=item.medicine_id,total_amount=total_amt, quantity=item.quantity)
        # order_item.save()
        # total_prices = item.medicine_id.price * item.medicine_id.quantity 
    return render(request, 'user/payment1.html', {'order_item': order_item,'total_price':Ttl_amounts})



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
    order_status = order_delivery.objects.filter(order_id__in=order_items)
    
    items_per_page = 10
    paginator = Paginator(order_status, items_per_page)
    page = request.GET.get('page', 1)

    try:
        order_status = paginator.page(page)
    except PageNotAnInteger:
       
        order_status = paginator.page(1)
    except EmptyPage:

        order_status = paginator.page(paginator.num_pages)
    context={
        
        'order_status': order_status,
    }
    
    return render(request, 'user/order_delivery.html',context)

def order_history(request):
    datas = CustomeUser.objects.get(id=request.user.id)
    category = Category.objects.all()
    order_items = order.objects.filter(user_id=datas)
    items_per_page = 5
    paginator = Paginator(order_items,items_per_page)
    page = request.GET.get('page', 1)

    try:
        order_items = paginator.page(page)
    except PageNotAnInteger:
       
        order_items = paginator.page(1)
    except EmptyPage:

        order_items = paginator.page(paginator.num_pages)
        
    context = {
        'order_items':order_items,
        'category':category,
        
    }
    return render(request, 'user/order_history.html',context)


def filteration(request):
    category = Category.objects.all()
    order_items = medicine.objects.all()
    
    # Apply filtering if the method is POST (when user selects categories)
    if request.method == 'POST':
        selected_categories = request.POST.getlist('categories')
        order_items = order.objects.filter(medicine_id__category_name__in=selected_categories)
    
    # Pagination
    items_per_page = 5
    paginator = Paginator(order_items, items_per_page)
    page = request.GET.get('page', 1)

    try:
        order_items = paginator.page(page)
    except PageNotAnInteger:
        order_items = paginator.page(1)
    except EmptyPage:
        order_items = paginator.page(paginator.num_pages)
    
    context = {
        'order_items': order_items,
        'category': category,
    }

    return render(request, 'user/order_history.html', context)

# def order_delivery_history(request):
#     datas = CustomeUser.objects.get(id=request.user.id)
#     order_items = order.objects.filter(user_id=datas)
    
#     return render(request, 'user/order_delivery.html',{'order_items':order_items})




def remove_orderview(request,id):
   
    order_del =  order.objects.get(id=id)
    order_del.delete()
    return redirect(order_history)

def pharmacy_user(request,id):
    user= CustomeUser.objects.get(id=request.user.id)
    pharmacy=CustomeUser.objects.get(id=id)
    

####debitt card system######
def Debitcard(request):
    user = CustomeUser.objects.get(id=request.user.id)
    order_item = cart.objects.filter(user_id=user)
    Ttl_amounts=0
    for item in order_item:
     
        total_amt=(item.medicine_id.price*item.quantity)
        Ttl_amounts+=total_amt
    if request.method == 'POST':
        cardholder_name = request.POST.get('cardholder_name')
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        
        for item in order_item:
            order_item = order.objects.create(
                    user_id=user,
                    medicine_id=item.medicine_id,
                    total_amount=Ttl_amounts,
                    quantity=item.quantity  
                )
            order_item.save()
        return redirect('order_confirmation')
    
    else:
        return render(request, 'user/Debit_card.html',{'order_item':order_item,'total_price':Ttl_amounts})
    
def cash_on_delivery(request):
    user = CustomeUser.objects.get(id=request.user.id)
    order_item = cart.objects.filter(user_id=user)
    Ttl_amounts=0
    for item in order_item:
     
        total_amt=(item.medicine_id.price*item.quantity)
        Ttl_amounts+=total_amt
    
        order_item = order.objects.create(
                    user_id=user,
                    medicine_id=item.medicine_id,
                    total_amount=Ttl_amounts,
                    quantity=item.quantity  
                )
        order_item.save()
        print(item.medicine_id)
        item.delete()
        
    # Return the response after the loop
    return render(request, 'user/cash_on_delivery.html', {'cart_items': order_item})

#   #***********pharmacy**********

def pharm_register(request):
    if request.method == 'POST':
            print("ss")
            name = request.POST['name']
            email = request.POST['Email']
            if CustomeUser.objects.filter(email=email).exists():
             return render(request,'pharmacy/registerp.html',{'error':'email already exists'})
            address = request.POST['Address']
            # place = request.POST['place']
            phoneno = request.POST['Phonenumber']
            if CustomeUser.objects.filter(phone_number=phoneno).exists():
             return render(request,'pharmacy/registerp.html',{'error':'username already exists'})
            username = request.POST['Username']
            place=request.POST['place']
            if CustomeUser.objects.filter(username=username).exists():
             return render(request,'pharmacy/registerp.html',{'error':'username already exists'})
            password = request.POST['Password']
            Confirmpassword=request.POST['Confirmpassword']
            if password!=Confirmpassword:
             return render(request,'pharmacy/registerp.html',{'error':'password not matching'})
            Image=request.FILES['Image']
            certificate=request.FILES['certificate']
            # print(Image)
            data=CustomeUser.objects.create_user(email=email,first_name=name,Image=Image,place=place,address=address,phone_number=phoneno,password=password,certificate=certificate,username=username,usertype='pharmacy')
            data.save()
            return redirect(Login)
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
        data.place=request.POST['place']
        data.username=request.POST['UserName']
        if 'Image' in request.FILES:
            data.Image = request.FILES['Image']
        if 'certificate' in request.FILES:
            data.certificate = request.FILES['certificate']
            # print(f"Certificate uploaded: {data.certification}")
        data.save()
        return redirect(pharm_profile)
    else:
        return render(request,'pharmacy/edit_profilep.html',{'datas':data})
@login_required(login_url='Login')
def pharm_home(request):
    try:
        company= CustomeUser.objects.filter(usertype='company').count()
        Orders = order.objects.all().count()
        medicines = medicine.objects.all().count()
        # return render(request, 'pharmacy/homep.html',{'company':company,'Orders':Orders} )
        return render(request, 'pharmacy/homep.html',{'company':company,'Orders':Orders,'medicines':medicines} )
    except CustomeUser.DoesNotExist:
        return redirect(Login)



def add_medicine(request):
    data =CustomeUser.objects.get(id=request.user.id)
    datas = Category.objects.all()
    var1=CustomeUser.objects.get(usertype='company')
    if request.method == 'POST':
        # print("post")
        name = request.POST['medicineName']
        price = request.POST['Price']
        per_price=request.POST['Price per Unit']
        description = request.POST['description']
        description1 = request.POST['description1']
        description2 = request.POST['description2']
        manufacturer = request.POST['manufacturer']
        category = request.POST['category']
        categoryid = Category.objects.get(id=category)
        quantity = request.POST['quantity']
        expiry_date = request.POST['expiryDate']
        strength=request.POST['strength']
        # print("strength:" ,strength)
        Image=request.FILES['Image']
        Image1=request.FILES['Image1']
        Image2=request.FILES['Image2']
        Image3=request.FILES['Image3']
        # print(Image)
        medicine_data = medicine.objects.create( pharmacy_id=data,name=name,Image=Image,price=price, per_price=per_price,Image1=Image1,Image2=Image2,Image3=Image3,description1=description1,description2=description2,strength=strength,description=description,manufacturer=manufacturer,quantity=quantity,category_name=categoryid.category_name,expiry_date=expiry_date)
        medicine_data.save()
        
        if 'perprice' in request.POST:
            medicine_data.perprice = request.POST['perprice']
            medicine_data.save()
        print(medicine_data.Image)
        print("save ",medicine_data)
        return redirect(pharm_home)
        # return HttpResponse ('medicine_view')
    else:
    
        return render(request, 'pharmacy/medicine1.html',{'datas': datas,'var1':var1})
        # return HttpResponse('sucessfuly')
   


def edit_medicine(request,id):
    data=medicine.objects.get(id=id)
    var1=CustomeUser.objects.get(usertype='company')
    datas = Category.objects.all()
    if request.method=='POST':
        data.name=request.POST['medicineName']
        data. price = request.POST['Price']
        data. per_price = request.POST['Price per Unit']
        data.description = request.POST['description']
        data.description1 = request.POST['description1']
        data.description2 = request.POST['description2']
        data.manufacturer = request.POST['manufacturer']
        data.quantity = request.POST['quantity']
        data.expiry_date = request.POST['expiryDate']
        data.strength=request.POST['strength']
        if 'Image' in request.FILES:
            data.Image = request.FILES['Image']
            data.Image1 = request.FILES['Image1']
            data.Image2 = request.FILES['Image2']
            data.Image3 = request.FILES['Image3']
        data.save()
        return redirect(medicine_viewpharma)
    else:
        return render(request,'pharmacy/edit_medicine.html',{'datas':data,'var1':var1,'data':datas})
    
    
def delete_med(request,id):   
    medicines = medicine.objects.get(id=id)
    medicines.delete()
    return redirect(medicine_viewpharma)
   
   
   
def medicine_viewss(request,id):
    medicines = medicine.objects.get(id=id)
    # print("image : ",medicines.Image)
    return render(request, 'pharmacy/viewmedicine.html',{'medicines': medicines})

def search_medicines_pharm(request):
    pharmacy=CustomeUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        search_query = request.POST.get('search', '')
        medicines = medicine.objects.filter(name__icontains=search_query,pharmacy_id=pharmacy)
        context = {'medicines': medicines,
                   'search_query': search_query,
                   'pharmacy':pharmacy}
        return render(request, 'pharmacy/med1.html', context)
    else: 
        return render(request, 'pharmacy/med1.html', {'medicines': medicine.objects.all()})
  
def contact_us(request):
    return render(request,'user/contact.html')

def medicine_viewpharma(request):
    medicines = medicine.objects.filter(pharmacy_id=request.user.id)
    
    items_per_page = 6
    paginator = Paginator(medicines,items_per_page)
    page = request.GET.get('page', 1)

    try:
        medicines = paginator.page(page)
    except PageNotAnInteger:
       
        medicines = paginator.page(1)
    except EmptyPage:

        medicines = paginator.page(paginator.num_pages)
        
    context = {
        'medicines':medicines,
        
    }
    
    
    return render(request, 'pharmacy/med1.html',context)

def view_cpny_med(request):
    prdts=product.objects.all()
    print(prdts)
    return render(request,'pharmacy/company_product.html',{'prdts':prdts})

def view_eachPrdt(request,id):
    prdts = product.objects.get(id=id)
    return render(request, 'user/medicinuser_view.html',{'prdts': prdts})

def order_product(request,id):
    product1 = product.objects.get(id=id)
    if request.method == "POST":
        quantity= request.POST['Quantity']
        var=int(product1.price)*int(quantity)
        context={
            'product':product1,
            'var':var,
            'quantity':quantity
        }
        return render(request,'pharmacy/order_view.html',context)
    else:
        return redirect(view_cpny_med)
    

def pharmacy_pharmacy(request,id,price,q):
    pharmacy=CustomeUser.objects.get(id=request.user.id)
    products=product.objects.get(id=id)
    
    data = company_order.objects.create(pharmacy_id=pharmacy,
                                        product_id=products,
                                        quantity=q,
                                        total_amount=price)
    data.save()
    # return HttpResponse("success")    
    return render(request,'pharmacy/order_comformed.html')

def company_history(request):
    pharmacy=CustomeUser.objects.get(id=request.user.id)
    cmpny_histry=company_order.objects.filter(pharmacy_id=pharmacy)
    return render (request, 'pharmacy/company_history.html',{'cmpny_histry':cmpny_histry})
########user>>>order all>>pharmacy seen ########
def pharmacy_vieworder(request):
    pharmacy_user = CustomeUser.objects.get(id=request.user.id)
    pharmacy_medicines = medicine.objects.filter(pharmacy_id=pharmacy_user)
    Orders = order.objects.filter(medicine_id__in=pharmacy_medicines).order_by('-id')
    
    items_per_page = 5
    paginator = Paginator(Orders,items_per_page)
    page = request.GET.get('page', 1)

    try:
        Orders = paginator.page(page)
    except PageNotAnInteger:
       
        Orders = paginator.page(1)
    except EmptyPage:

        Orders = paginator.page(paginator.num_pages)
        
    context = {
    
        'Orders': Orders, 
        'pharmacy_medicines': pharmacy_medicines
    }

    
    return render(request, 'pharmacy/userorder_get.html',context)

def userorder_view(request,id):
    data =  order.objects.get(id=id)
    # total_price
    
    return render(request,'pharmacy/viewone_order.html',{'data':data})

 
def chek_user_delivery(request, id):
    data = order.objects.get(id=id)
    delivery = CustomeUser.objects.filter(usertype = "delivery")
    delivary1 = Delivary.objects.filter(delivary_id__in=delivery.values_list('id', flat=True),status="Available")
    return render(request, 'pharmacy/delivery.html', {'delivery': delivary1,'data':data})

def search_delivery(request,id):
    data = order.objects.get(id=id)
    delivery = CustomeUser.objects.filter(usertype = "delivery")
    delivary1 = Delivary.objects.filter(delivary_id__in=delivery.values_list('id', flat=True),status="Available")
    if request.method == 'POST':
        search_query = request.POST.get('search', '')
        delivary1 = Delivary.objects.filter(address__icontains=search_query,status="Available")
        # delivery_address =CustomeUser.objects.a
        context = {'delivery': delivary1,
                   'search_query': search_query, 
                   'data':data,  
                  }
        return render(request, 'pharmacy/delivery.html', context)
    else: 
        context = {'delivery': delivary1,
                   'search_query': search_query, 
                   'data':data,  
                  }
        return render(request, 'pharmacy/delivery.html',context)

    
def Assign_delivery(request,id,a):  
    pharmacy1=CustomeUser.objects.get(id=request.user.id)
    order1=order.objects.get(id=a)
    delivery1=Delivary.objects.get(id=id)
    data=order_delivery.objects.create(pharmancy_id=pharmacy1,order_id=order1,delivery_id=delivery1)
    data.save()
    
    return redirect(user_history_page)

def user_history_page(request):
    history = order_delivery.objects.filter(pharmancy_id=request.user.id)
    return render(request, 'pharmacy/user_history.html', {'history': history})
    
def pharmacy_prescription(request):
    data = CustomeUser.objects.get(id=request.user.id)
    prescp=prescription.objects.filter(pharmancy_id=data.id)
    return render(request,'pharmacy/prescription_upld.html',{'data':prescp})
 



def pharmacy_history(request):
    return render(request,'pharmacy/historypage1.html')






#*****************delivery**********
def delivery_Register(request):
    if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['Email']
            if Delivary.objects.filter(email=email).exists():
                return render(request,'delivery/dlvy_register.html',{'error':'email already exists'})
            address = request.POST['Address']
            phoneno = request.POST['Phonenumber']
            if Delivary.objects.filter(phonenumber=phoneno).exists():
                return render(request,'delivery/dlvy_register.html',{'error':'username already exists'})
            Age = request.POST['Age']
            dob = request.POST['DOB']
            username = request.POST['UserName']
            if CustomeUser.objects.filter(username=username).exists():
             return render(request,'delivery/dlvy_register.html',{'error':'username already exists'})
            password = request.POST['Password']
            Confirmpassword=request.POST['Confirmpassword']
            if password!=Confirmpassword:
             return render(request,'delivery/dlvy_register.html',{'error':'password not matching'})
            image=request.FILES['Image']
            License=request.FILES['license']
            data=CustomeUser.objects.create_user(password=password,
                                                username=username,
                                                email=email,
                                                 usertype='delivery')
            data.save()
            # print(data, "dtaaaaaa")
            data1 = Delivary.objects.create(delivary_id=data,name=name,dob=dob,image=image,email=email,licence=License,address=address,phonenumber=phoneno,age=Age)
            data1.save()
            return render(request,'login.html')
    else:
           return render(request,'delivery/dlvy_register.html')
       
       
def deliver_profile(request):
    data=CustomeUser.objects.get(id=request.user.id)
    datas=Delivary.objects.get(delivary_id=data)
    return render(request,'delivery/delivery_profile.html',{'datas':datas,'data':data})

def edit_delivery(request):
    data=CustomeUser.objects.get(id=request.user.id)
    data1=Delivary.objects.get(delivary_id=data)

    if request.method=='POST':
        print("post")
        data1.name=request.POST['Name']
        data1.phonenumber=request.POST['Phonenumber']
        data1.address=request.POST['Address']
        data1.email=request.POST['Email'] 
        data.username=request.POST['UserName']
        if 'Image' in request.FILES:
            data1.image = request.FILES['Image']
        if 'Licence' in request.FILES:
            data1.licence = request.FILES['Licence']
        data.save()
        data1.save()
        return redirect(deliver_profile)
    else:
        return render(request,'delivery/profile_edit.html',{'data1':data1,'data':data})


@login_required(login_url='Login')
def deliver_home(request):
    try:
        # data=order.objects.filter(id=request.user.id).count()
        delivary_user = CustomeUser.objects.get(id=request.user.id)
        delivary_user1 = Delivary.objects.get(delivary_id=delivary_user)
    
        # return render(request,'user/delivery_order.html',{'pharmacy_user':pharmacy_user})
        return render(request,'delivery/delivery_home.html',{'delivary_user1':delivary_user1})
    except CustomeUser.DoesNotExist:
        return redirect(Login)

def delivr_order_user(request):
    # Orders = order.objects.all()
    return render(request,'delivery/user_order.html')

########################extra.....
def delivr_wallect(request):
    return render(request,'delivery/user_order.html')

def delivr_history(request):
    
    return render(request,'delivery/user_history.html')

def delivery_available(request,id):
    data=Delivary.objects.get(id=id)
    print("data: ",data)
    if request.method=="POST":
        status=request.POST.get('status')
        print("")
        if status=='Available':
            data.status = "Available"
        elif status=="Not Available":
            data.status ="Not Available"
        data.save()
        return redirect(deliver_home)
    else:
        return redirect(deliver_home)
        
def delivery_order_view(request):
    data1 = CustomeUser.objects.get(id=request.user.id)
    data2 = Delivary.objects.get(delivary_id=data1)
    datas=order_delivery.objects.filter(delivery_id=data2)
    for i in datas:
        print(i)
    return render(request,'delivery/delivery_order.html',{'datas':datas}) 
    
def status_delivery(request,id):
    data=order_delivery.objects.get(id=id)
    if request.method=="POST":
        value=request.POST['status']
        if value=="STARTED":
            data.status=value
        elif value=="finished":
            data.status=value
        data.save()
        return redirect(delivery_order_view)
    else:
        return redirect(delivery_order_view)

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
            image=request.FILES['Image']
            certificate=request.FILES['certificate']
            data=CustomeUser.objects.create_user(first_name=name,email=email,Image=image,certificate=certificate,address=address,phone_number=phoneno,password=password,username=username,usertype='company')
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
        if 'Image' in request.FILES:
            data.Image = request.FILES['Image']
        data.save()
        return redirect(company_profile)
    else:
        return render(request,'company/company_editprofile.html',{'datas':data})
############extra company
@login_required(login_url='Login')
def company_home(request):
    try:
        Products= product.objects.filter(company_id=request.user.id)
        return render(request, 'company/company_home.html',{'Products': Products})
    except CustomeUser.DoesNotExist:
        return redirect(Login)
def add_product(request):
    data =CustomeUser.objects.get(id=request.user.id)
    if request.method == 'POST':
        name = request.POST['product_name']
        price = request.POST['price']
        description = request.POST['description']
        quantity = request.POST['quantity']
        Image=request.FILES['Image']
        medicine_data = product.objects.create(company_id=data,name=name,Image=Image,price=price,description=description,quantity=quantity)
        medicine_data.save()

    return render(request,'company/add_product.html')

def product_view(request,id):
    products=product.objects.get(id=id)
    return render(request,'company/view_each.html',{'products':products})

def view_all(request):
    Products= product.objects.filter(company_id=request.user.id)
    return render(request, 'company/view_product.html',{'Products': Products})
    
    
def edit_Product(request,id):
    data=product.objects.get(id=id)
    if request.method=='POST':
        data.name=request.POST['product_name']
        data. price = request.POST['price']
        data.description = request.POST['description']
        data.quantity = request.POST['quantity']
        if 'Image' in request.FILES:
            data.Image = request.FILES['Image']
        data.save()
        return redirect(view_all)
    else:
        return render(request,'company/edit_product.html',{'datas':data})
    
    
def delete_product(request,id):   
    products = product.objects.get(id=id)
    products.delete()
    return redirect(view_all)
   
def order_view_company(request):
   
    company=company_order.objects.all()
    return render(request,'company/order_view_company.html',{'company':company})

    
def company_status(request,id): 
    company=company_order.objects.get(id=id)
    if request.method=="POST":
        value=request.POST['status']
        if value=="ACCEPT":
            company.status=value
        elif value=="REJECT":
            company.status=value
        company.save()
        return redirect(order_view_company)
    else:
        return redirect(order_view_company)

####admin####
@login_required(login_url='Login')
def admin_home(request):
    try:
        catogory = Category.objects.all()
        for i in catogory:
            print(i.category_name)
        strengths = medicine.objects.values('strength').distinct()
        # data = CustomeUser.objects.filter(status="pending" )
        # print(data)
        user = CustomeUser.objects.filter(usertype='user').count()
        pharmacy = CustomeUser.objects.filter(usertype='pharmacy').count()
        delivery = CustomeUser.objects.filter(usertype='delivery').count()
        medicines = medicine.objects.all().count()
        
        context = {
                    'catogory':catogory,
                    'strengths':strengths,
                    'user':user,
                    'pharmacy':pharmacy,
                    'delivery':delivery,
                    'medicines':medicines
                    }
        return render(request,'admin/home.html',context)
    except CustomeUser.DoesNotExist:
        return redirect(Login)


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
            # return redirect(admin)
            return HttpResponse("sucess")




def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        
        password = request.POST['password']
        admin_user = authenticate(request, username=username, password=password)
        if admin_user is not None and admin_user.is_staff:
                login(request,admin_user)
                #  Authenticate superusers (admins)
                # return redirect('admin:index')  # Redirect to the admin dashboard
                return redirect(admin_home)
        else:
            context = {
                'message': "Invalid credentials"
            }
            return render(request, 'admin/index.html',context)
    else: 
        return render(request,'admin/index.html')


def admin_custumer(request):
    Customer=CustomeUser.objects.filter(usertype='user')
    items_per_page = 1
    paginator = Paginator(Customer, items_per_page)
    page = request.GET.get('page', 1)

    try:
        Customer = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        Customer = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results
        Customer = paginator.page(paginator.num_pages)
    context={
        'Customer': Customer
    }
    return render(request,'admin/custmer.html',context)
 
 
 
def admin_view_custmer(request):
    customers=CustomeUser.objects.filter(usertype='user')
    items_per_page = 1
    paginator = Paginator(customers, items_per_page)
    page = request.GET.get('page', 1)

    try:
        customers = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        customers = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver the last page of results
        customers = paginator.page(paginator.num_pages)
    context={
        'customers': customers
    }
    return render(request,'admin/view_custmer.html',context)



def admin_pharmacy(request):
    pharmacy=CustomeUser.objects.filter(usertype='pharmacy')
    items_per_page = 1
    paginator = Paginator(pharmacy, items_per_page)
    page = request.GET.get('page', 1)

    try:
        pharmacy = paginator.page(page)
    except PageNotAnInteger:
       
        pharmacy = paginator.page(1)
    except EmptyPage:

        pharmacy = paginator.page(paginator.num_pages)
    context={
        'pharmacy': pharmacy
    }
    return render(request,'admin/pharm_list.html',context)




def admin_view_pharmacy(request):
    pharmacys=CustomeUser.objects.filter(usertype='pharmacy')
    items_per_page = 1
    paginator = Paginator(pharmacys, items_per_page)
    page = request.GET.get('page', 1)

    try:
        pharmacys = paginator.page(page)
    except PageNotAnInteger:
       
        pharmacys = paginator.page(1)
    except EmptyPage:

        pharmacys = paginator.page(paginator.num_pages)
    context={
        'pharmacys': pharmacys
    }
    return render(request,'admin/pham_view.html',context)

def admin_delivery(request):
    # Customer=CustomeUser.objects.filter(usertype='delivery')
    # # Customer=CustomeUser.objects.all()
    # return redirect(request,'admin/.html',{'Customer':Customer})
    delivery = CustomeUser.objects.filter(usertype = "delivery")
    delivary1 = Delivary.objects.filter(delivary_id__in=delivery)
    
    items_per_page = 1
    paginator = Paginator(delivary1, items_per_page)
    page = request.GET.get('page', 1)

    try:
        delivary1 = paginator.page(page)
    except PageNotAnInteger:
       
        delivary1 = paginator.page(1)
    except EmptyPage:

        delivary1 = paginator.page(paginator.num_pages)
    context={
        'delivary1': delivary1
    }
    
    return render(request, 'admin/deliver_list.html',context)



def admin_delivery_view(request):
    deliverys = CustomeUser.objects.filter(usertype = "delivery")
    delivarys1 = Delivary.objects.filter(delivary_id__in=deliverys)
    items_per_page = 1
    paginator = Paginator(delivarys1, items_per_page)
    page = request.GET.get('page', 1)

    try:
        delivarys1 = paginator.page(page)
    except PageNotAnInteger:
       
        delivarys1 = paginator.page(1)
    except EmptyPage:

        delivarys1 = paginator.page(paginator.num_pages)
    context={
        'delivarys1': delivarys1
    }
    return render(request, 'admin/delivery_view.html', context)

#####view on each action####

######customer
def admin_user_view(request,id):
    data = CustomeUser.objects.get(id=id)
    return render (request ,'admin/profile_view.html',{'data':data})
def admin_edit_customer(request,id):
    data = CustomeUser.objects.get(id=id)
    if request.method=='POST':
        data.first_name=request.POST['first_name']
        data.address=request.POST['address']
        data.email=request.POST['email']  
        data.dob=request.POST['dob']  
        if 'Image' in request.FILES:
            data.Image = request.FILES['Image']
        data.save()
        return redirect(admin_user_view)
    else:
        return render (request,'admin/edit_customer.html',{'data':data} )
   
def admin_delete_customer(request,id):
    data = CustomeUser.objects.get(id=id)
    data.delete()
    return redirect(admin_view_custmer)

    
 ######pharmacy   
def admin_pharmacy_view(request,id):
    
    data1 = CustomeUser.objects.get(id=id)

    return render (request ,'admin/pharm_profile.html',{'data1':data1})
        
def admin_edit_pharmacy(request,id):
    data = CustomeUser.objects.get(id=id)
    if request.method=='POST':
        data.first_name=request.POST['Name']
        data.phone_number=request.POST['Phonenumber']
        data.address=request.POST['Address']
        data.email=request.POST['Email']  
        data.place=request.POST['place']
        data.username=request.POST['UserName']
        if 'Image' in request.FILES:
            data.Image = request.FILES['Image']
        if 'certificate' in request.FILES:
            data.certificate = request.FILES['certificate']
            # print(f"Certificate uploaded: {data.certification}")
        data.save()
        return redirect(admin_pharmacy_view)
    else:
        return render (request,'admin/edit _pharm.html',{'data':data} )

def admin_delete_pharmacy(request,id):
    datas = CustomeUser.objects.get(id=id)
    datas.delete()
    return redirect(admin_view_pharmacy)

 
######delivery
    
def admin_delvry_viewone(request,id):
    # data1 = CustomeUser.objects.get(id=id)
   
    
    deliverys = Delivary.objects.get(id=id)
    delivarys1 = CustomeUser.objects.get(id=deliverys.delivary_id.id)
    context={
        
        'deliverys':deliverys,
        'delivarys1':delivarys1
        
    }
    return render(request ,'admin/viewone_delivery.html',context)

    
    



def admin_edit_delivery(request,id):
    delivery = Delivary.objects.get(id=id)
    data=CustomeUser.objects.get(id=delivery.delivary_id.id)

    if request.method=='POST':
        data.name=request.POST['Name']
        data.phonenumber=request.POST['Phonenumber']
        data.address=request.POST['Address']
        data.email=request.POST['Email'] 
        data.username=request.POST['UserName']
        if 'Image' in request.FILES:
            data.image = request.FILES['Image']
        if 'Licence' in request.FILES:
            data.licence = request.FILES['Licence']
        delivery.save()
        data.save()
        return redirect()
    else:
        return render (request,'admin/.html',{'data':data} )



def admin_delete_delivery(request,id):
    delivery = Delivary.objects.get(id=id)
    data=CustomeUser.objects.get(id=delivery)
    data.delete()
    return redirect(admin_delivery_view)



def admin_add_category(request):
    if request.method == 'POST':
         category_name = request.POST['category_name']
         data = Category.objects.create(category_name=category_name)
         data.save()
         return redirect(admin_category_list)
    else:
        return render(request,'admin/admin_category.html')
         

def admin_category_list(request):
    strengths = medicine.objects.values('strength').distinct()
    category = Category.objects.all()
    return render(request,'admin/category_list.html',{'catogory':category,'strengths':strengths})


def admin_delete_catagory(request,id):
    datas = Category.objects.get(id=id)
    datas.delete()
    return redirect(admin_category_list)

def admin_category_search(request):
    if request.method=='POST':
        catogory = request.POST['category']
        medicines=medicine.objects.filter(category_name=catogory)
        return render(request,'admin/admin_search.html',{'medicines':medicines})
    else:
        return redirect(admin_home)

def admin_product(request):
     medicines = medicine.objects.all()
     return render(request,'admin/admin_product.html',{'medicines':medicines})
def admin_contact(request):
    data=ContactUs.objects.all()
    return render (request,'admin/admin_contact.html',{'data':data})