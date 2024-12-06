import json
from itertools import product, count
from symtable import Class

# from django.core.serializers import json
from django.http import JsonResponse
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaultfilters import title
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from pyexpat.errors import messages
from django.http import JsonResponse
from .forms import CustomerRegistrationForm, CustomerProfileForm
from .models import Product, Customer, Cart, Wishlist
from .forms import CustomerRegistrationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

class CategoryView(View):
    def get(self,request,val):
        product = Product.objects.filter(category=val)
        title =Product.objects.filter(category=val).values('title').annotate(total=Count('title'))
        return render(request, 'category.html',locals())

class CategoryTitle(View):
    def get(self,request,val):
        product = Product.objects.filter(title=val)
        title =Product.objects.filter(category=val).values('title')
        return render(request, 'category.html',locals())


class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        return render(request,"productdetail.html",locals())

class CustomerRegistrationView(View):
    def get(self, request):
        form= CustomerRegistrationForm()
        return render(request, 'customerregistration.html',locals())
    def post(self,request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Congratulations! User Registration Successfully')
        else:
            messages.warning(request, 'Invalid Input Data')
        return render(request, 'customerregistration.html', locals())


class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        return render(request, 'profile.html',locals())
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            town = form.cleaned_data['town']
            zipcode = form.cleaned_data['zipcode']

            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, town=town,
                           zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Save Successfully")
        else:
            messages.warning(request, "Invalid Input Data")

        return render(request, 'profile.html', locals())

def address(request):
    add = Customer.objects.filter(user=request.user)
    return render(request,'address.html',locals())

class updateAddress(View):
    def get(self, request,pk):
        add= Customer.objects.get(pk=pk)
        form=CustomerProfileForm(instance=add)
        return render(request, 'updateAddress.html', locals())
    def post(self, request,pk):
        form=CustomerProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.town = form.cleaned_data['town']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile Updated Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect("address")


def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/cart")

# def show_cart(request):
#     user = request.user
#     cart = Cart.objects.filter(user=user)
#     return render(request, 'addtocart.html', locals())
@login_required
def show_cart(request):
    user = request.user

    # Ensure cart items exist
    cart = Cart.objects.filter(user=user)

    if not cart.exists():
        # If no items in cart, render with an empty cart message
        return render(request, 'addtocart.html', {'cart': None})

    # Calculate total amounts
    amount = sum(item.product.discounted_price * item.quantity for item in cart)
    shipping_cost = 40  # Fixed shipping cost
    total = amount + shipping_cost

    # Pass data to the template
    context = {
        'cart': cart,
        'amount': amount,
        'total': total
    }
    return render(request, 'addtocart.html', context)
def update_cart_quantity(request):
    if request.method == 'POST' and request.is_ajax():
        product_id = request.POST.get('product_id')
        action = request.POST.get('action')

        try:
            cart_item = Cart.objects.get(user=request.user, product_id=product_id)

            # Update quantity based on the action
            if action == 'increase':
                cart_item.quantity += 1
            elif action == 'decrease' and cart_item.quantity > 1:
                cart_item.quantity -= 1

            cart_item.save()

            # Calculate totals
            cart_total = sum(item.product.discounted_price * item.quantity for item in Cart.objects.filter(user=request.user))
            item_total = cart_item.product.discounted_price * cart_item.quantity

            return JsonResponse({
                'status': 'success',
                'item_quantity': cart_item.quantity,
                'item_total': item_total,
                'cart_total': cart_total,
            })

        except Cart.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Cart item does not exist'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def update_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data["product_id"]
        action = data["action"]

        # Logic for updating the cart
        cart_item = Cart.objects.get(user=request.user, product_id=product_id)
        if action == "plus":
            cart_item.quantity += 1
        elif action == "minus" and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()

        # Calculate totals
        cart_items = Cart.objects.filter(user=request.user)
        amount = sum(item.product.discounted_price * item.quantity for item in cart_items)
        total = amount + 40  # Add shipping fee

        return JsonResponse({
            "success": True,
            "new_quantity": cart_item.quantity,
            "item_total": cart_item.product.discounted_price * cart_item.quantity,
            "amount": amount,
            "total": total
        })
# def update_cart(request, pid, action):
#     cart = Cart.objects.get(user=request.user)
#     product = Product.objects.get(id=pid)
#
#     if action == 'add':
#         cart_item = cart.items.get(product=product)
#         cart_item.quantity += 1
#         cart_item.save()
#     elif action == 'subtract':
#         cart_item = cart.items.get(product=product)
#         cart_item.quantity -= 1
#         cart_item.save()
#         if cart_item.quantity == 0:
#             cart_item.delete()
#     elif action == 'remove':
#         cart.items.get(product=product).delete()
#
#     # Recalculate cart totals
#     cart_total = sum(item.product.discounted_price * item.quantity for item in cart.items.all())
#     cart_count = sum(item.quantity for item in cart.items.all())
#
#     return JsonResponse({
#         'cart_count': cart_count,
#         'cart_amount': cart_total + 40,  # Assuming shipping is 40
#         'cart_total': cart_total + 40,
#         'item_total': product.discounted_price * cart_item.quantity if action != 'remove' else 0,
#         'quantity': cart_item.quantity if action != 'remove' else 0,
#     })

def remove_cart(request):
    if request.method == "POST":
        data = json.loads(request.body)
        product_id = data["product_id"]

        # Logic for removing the cart item
        Cart.objects.filter(user=request.user, product_id=product_id).delete()

        # Calculate totals
        cart_items = Cart.objects.filter(user=request.user)
        amount = sum(item.product.discounted_price * item.quantity for item in cart_items)
        total = amount + 40  # Add shipping fee

        return JsonResponse({
            "success": True,
            "amount": amount,
            "total": total
        })

import requests

from django.views.decorators.csrf import csrf_exempt
import datetime
from django.conf import settings

    # Generate Access Token
def get_mpesa_access_token():
        consumer_key = settings.MPESA_CONSUMER_KEY
        consumer_secret = settings.MPESA_CONSUMER_SECRET
        auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
        return response.json()["access_token"]

    # STK Push View
@csrf_exempt
def stk_push(request):
        if request.method == "POST":
            phone = request.POST.get("phone")  # Phone number from user input
            amount = request.POST.get("amount")  # Total amount
            access_token = get_mpesa_access_token()

            # MPesa STK Push API
            stk_push_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization": f"Bearer {access_token}"}
            payload = {
   "BusinessShortCode": "174379",
   "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMTYwMjE2MTY1NjI3",
   "Timestamp":"20160216165627",
   "TransactionType": "CustomerPayBillOnline",
   "Amount": "1",
   "PartyA":"254708374149",
   "PartyB":"174379",
   "PhoneNumber":"254742048713",
   "CallBackURL": "https://strong-oarfish-evident.ngrok-free.app",
   "AccountReference":"Test",
   "TransactionDesc":"Test"
 }
            response = requests.post(stk_push_url, json=payload, headers=headers)
            return JsonResponse(response.json())

        return JsonResponse({"error": "Invalid request method"}, status=400)
@csrf_exempt
def mpesa_callback(request):
    if request.method == "POST":
        data = request.body.decode("utf-8")
        print("Callback Data:", data)  # Process and save the data as needed
        return JsonResponse({"message": "Received callback successfully"})

    return JsonResponse({"error": "Invalid request method"}, status=400)





@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

@login_required
def add_to_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.get_or_create(user=request.user, product=product)
    return redirect('wishlist')

@login_required
def remove_from_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect('wishlist')
