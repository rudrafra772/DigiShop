import imp
from pickle import FALSE
from urllib import request
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views import View
from .models import Customer, Product, Cart, OrderPlaced
from .forms import CustomerRegistrarionForm, CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib import humanize
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


#def home(request):
# return render(request, 'app/home.html')

def cart_item(request,format=None):
    total_item = 0
    total_item = len(Cart.objects.filter(user = request.user))
    return total_item


class ProductView(View):
    def get(self,request):
        allproduct = Product.objects.all()
        mobile = Product.objects.filter(category='M')
        laptop = Product.objects.filter(category='L')
        topwear = Product.objects.filter(category='TW')
        bottomwear = Product.objects.filter(category='BW')
        return render(request,'app/home.html',
        {'moblie':mobile,
        'laptop':laptop,
        'topweare':topwear,
        'bottomwear':bottomwear,
        'allproduct':allproduct,
        'cart_item':cart_item(request)
        }
        )




#def product_detail(request):
 #return render(request, 'app/productdetail.html')


class Product_DetailView(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        item_in_cart = FALSE
        if request.user.is_authenticated:
            item_in_cart = Cart.objects.filter(Q(product= product.id) & Q(user=request.user)).exists()
        return render(request, 'app/productdetail.html',{'product':product, 'item_in_cart':item_in_cart,
        'cart_item':cart_item(request)})


@login_required
def add_to_cart(request):
    if request.user.is_authenticated:
        user=request.user
        product_id = request.GET.get('prod_id')
        product = Product.objects.get(id=product_id)
        Cart(user=user, product=product).save()
        return redirect('/cart')
    else:
        return redirect('/accounts/login')


@login_required
def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 70.0
        totalamoutn = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
                totalamoutn = amount + shipping_amount
            return render(request, 'app/addtocart.html',{'carts':cart, 'totalamount':totalamoutn, 'amount':amount,
        'cart_item':cart_item(request)})
        else:
            return render(request, 'app/emptycart.html')
    

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount

        data={
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount + shipping_amount
            }        
        return JsonResponse(data)    

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount

        data={
                'quantity': c.quantity,
                'amount': amount,
                'totalamount': amount + shipping_amount
            }        
        return JsonResponse(data)


def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = 0.0
        shipping_amount = 70.0
        cart_product = [p for p in Cart.objects.all() if p.user == request.user]
        for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount

        data={
                'amount': amount,
                'totalamount': amount + shipping_amount
            }        
        return JsonResponse(data) 


@login_required
def buy_now(request):
 return render(request, 'app/buynow.html')


@login_required
def orders(request):
    op = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html', {'order_placed':op,
        'cart_item':cart_item(request)})

#def change_password(request):
# return render(request, 'app/changepassword.html')

def mobile(request, data=None):
    if data == None:
        mobiles = Product.objects.filter(category='M')
    elif data == 'Samsung' or data =='Apple':
        mobiles =  Product.objects.filter(category='M').filter(brand=data)
    elif data == 'bellow':
        mobiles =  Product.objects.filter(category='M').filter(discounted_price__lt=15000)
    elif data == 'above':
        mobiles =  Product.objects.filter(category='M').filter(discounted_price__gt=10000)
    
    return render(request, 'app/mobile.html', {'mobiles':mobiles,
        'cart_item':cart_item(request)})

#def login(request):
# return render(request, 'app/login.html')

#def customerregistration(request):
 #return render(request, 'app/customerregistration.html')

class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrarionForm()
        return render(request, 'app/customerregistration.html',{'form':form})
    def post(self, request):
        form = CustomerRegistrarionForm(request.POST)
        if form.is_valid():
            messages.success(request, 'Congralutions!! Registered Successfully')
            form.save()
        return render(request, 'app/customerregistration.html',{'form':form,
        'cart_item':cart_item(request)})

@login_required
def checkout(request):
    user = request.user
    add = Customer.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    amount = 0.0
    shipping_amount = 70.0
    totalamount = 0.0
    cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:  
            tempamount = (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount + shipping_amount
    return render(request, 'app/checkout.html', {'add':add, 'totalamount':totalamount, 'cart_items':cart_items,
        'cart_item':cart_item(request)})


@login_required
def payment_done(request):
    user = request.user
    custid = request.GET.get('custid')
    customer = Customer.objects.get(id = custid)
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer, product=c.product, quantity=c.quantity).save()
        c.delete()
    return redirect("orders")


#def profile(request):
# return render(request, 'app/profile.html')
@login_required
def address(request):
 addr = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'addr':addr, 'active':'btn-primary',
        'cart_item':cart_item(request)})

@method_decorator(login_required, name='dispatch')
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        addr = Customer.objects.filter(user=request.user)
        return render(request, 'app/profile.html',{'form':form, 'active':'btn-primary', 'addr':addr,
        'cart_item':cart_item(request)})

    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            reg = Customer(user=usr, name=name, locality= locality, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, 'Congralutions!!! Profile Updated')
        return render(request, 'app/profile.html', {'form':form, 'active':'btn-primary',
        'cart_item':cart_item(request)})