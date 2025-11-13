from http.client import responses

from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator

from django.views import View
from django.views.decorators.csrf import csrf_exempt

from shop.models import Product

import razorpay
# Create your views here.

from cart.models import Cart

class Addtocart(View):
    def get(self,request,i):
        p=Product.objects.get(id=i)
        u=request.user
        try:
            c=Cart.objects.get(user=u,product=p)    #check whether the product already placed by current user
            c.quantity+=1                           #or checks whether product is there in cart table
            c.save()                                # if yes increment quantity by ine
        except:
            c=Cart.objects.create(user=u,product=p,quantity=1)  #else create new record inside cart table
            c.save()
        return redirect('cart:cartview')

class Cartview(View):
    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u) #filter cart items in selected by current user

        #to find total price
        total=0
        for i in c:
            total+=i.product.price*i.quantity
        context={'cart':c,'total':total}
        return render(request,'cart.html',context)

class Addquantity(View):
    def get(self,request,i):
        p = Product.objects.get(id=i)
        u = request.user
        try:
            c = Cart.objects.get(user=u, product=p)
            c.quantity += 1
            c.save()
        except:
            c = Cart.objects.create(user=u, product=p, quantity=1)
            c.save()
        return redirect('cart:cartview')

class Deletequantity(View):
    def get(self,request,i):
        p = Product.objects.get(id=i)
        u = request.user
        try:
            c = Cart.objects.get(user=u, product=p)
            if c.quantity > 1:
                c.quantity -= 1
                c.save()
            else:
                c.delete()
        except:
           pass
        return redirect('cart:cartview')

class Delete(View):
    def get(self, request, i):
        p = Product.objects.get(id=i)
        u = request.user
        try:
            c = Cart.objects.get(user=u, product=p)
            c.delete()
        except:
            pass
        return redirect('cart:cartview')

from cart.forms import Orderform


def checkstock(c):
    stock=True
    for i in c:
        if i.product.stock<i.quantity:
            stock=False
            break
    else:
        stock=True
    return stock

from django.contrib import messages
import uuid
class Checkout(View):
    def post(self,request):
        print(request.POST)
        form_instance=Orderform(request.POST)
        if form_instance.is_valid():
            o=form_instance.save(commit=False)
            u=request.user
            o.user=u
            c=Cart.objects.filter(user=u)
            total=0
            for i in c:
                total+=i.product.price*i.quantity
            o.amount=total
            o.save()
            if o.payment_method=='online':
                #razorpay clint connection
                client=razorpay.Client(auth=('rzp_test_RdvE8CPnsiqcrx','2gg1C7RpAJXUrMP4FfwRZ9pB'))         #('keyid','secretkey')
                #placeorder
                response_payment=client.order.create(dict(amount=total*100,currency='INR'))
                print(response_payment)
                id=response_payment['id']
                o.order_id=id
                o.save()
                context={'payment':response_payment}
                return render(request,'payment.html',context)


            else:#order COD
                o.is_ordered=True
                uid=uuid.uuid4().hex[:14]
                id='order_COD'+uid #manually creates orderid for COD orders using uuid module
                o.order_id=id
                o.save()

                # order_items
                c = Cart.objects.filter(user=u)

                for i in c:
                    o = Order_items.objects.create(order=o, product=i.product, quantity=i.quantity)
                    o.save()
                    o.product.stock -= o.quantity
                    o.product.save()

                # delete cart
                c.delete()
                return render(request, 'payment_success.html')

        return render(request, 'checkoutform.html')

    def get(self,request):
        u=request.user
        c=Cart.objects.filter(user=u)
        stock=checkstock(c)
        if stock:
            form_instance=Orderform()
            context={'form':form_instance}
            return render(request,'checkout.html',context)
        else:
            messages.error(request,'cant place order')
            return render(request,'checkout.html')

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth import login
from cart.models import Order,Order_items

#to avoid csrf verification we use csrf_exempt
@method_decorator(csrf_exempt,name="dispatch")

class Payment_success(View):
    def post(self,request,i): #i represent username
                              # to add into current session again
        u=User.objects.get(username=i)
        login(request,u)      #adds the user objects u into session
        response=request.POST #after payment razorpay send payment details into success view
                              #as response
        print(response)
        id=response['razorpay_order_id']
        print(id)
        #order
        order=Order.objects.get(order_id=id)
        order.is_ordered=True #after success completion of order
        order.save()
        #order items
        c=Cart.objects.filter(user=u)
        for i in c:
            o=Order_items.objects.create(order=order,product=i.product,quantity=i.quantity)
            o.save()
            o.product.stock-=o.quantity
            o.product.save()


        #cart deletion
        c.delete()

        return render(request,'payment_success.html')

class Your_orders(View):
    def get(self,request):
        u=request.user
        o=Order.objects.filter(user=u,is_ordered=True)
        context={'orders':o}
        return render(request,'your_order.html',context)
