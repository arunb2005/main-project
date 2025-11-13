from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from shop.models import Category,Product

from shop.forms import Signupform,Loginform

from shop.forms import Productform, Categoryform

from shop.forms import Stockform


# Create your views here.

class Categoryview(View):
    def get(self,request):
        s=Category.objects.all()
        context={'category':s}
        return render(request,'categories.html',context)

class Productview(View):
    def get(self,request,i):
        s=Category.objects.get(id=i)
        context={'category':s}
        return render(request,'productview.html',context)

class Productdetails(View):
    def get(self,request,j):
        p=Product.objects.get(id=j)
        context={'product':p}
        return render(request,'productdetails.html',context)


class Register(View):
    def post(self,request):
        form_instance=Signupform(request.POST)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:userlogin')
        else:
            context={'form':form_instance}
            return render(request,'register.html',context)

    def get(self,request):
        form_instance=Signupform()
        context={'form':form_instance}
        return render(request,'register.html',context)

class Login(View):
    def post(self,request):
        form_instance=Loginform(request.POST)
        if form_instance.is_valid():
            u=form_instance.cleaned_data['username']
            p=form_instance.cleaned_data['password']
            user=authenticate(username=u,password=p)
            if user and user.is_superuser == True:
                login(request, user)
                return redirect('shop:categories')
            elif user and user.is_superuser!=True:
                login(request, user)
                return redirect('shop:categories')
            else:
                context={'form':form_instance}
                return render(request,'userlogin.html',context)
    def get(self,request):
        form_instance=Loginform()
        context={'form':form_instance}
        return render(request,'userlogin.html',context)
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('shop:userlogin')

class Addproduct(View):
    def get(self,request):
        form_instance=Productform()
        context={'form':form_instance}
        return render(request,'addproduct.html',context)

    def post(self,request):
        form_instance=Productform(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:addproduct')

class Addcategory(View):
    def get(self,request):
        form_instance=Categoryform()
        context={'form':form_instance}
        return render(request,'addcategory.html',context)

    def post(self,request):
        form_instance=Categoryform(request.POST,request.FILES)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:addcategory')

class Updatestock(View):
    def post(self, request,i):
        p=Product.objects.get(id=i)
        form_instance = Stockform(request.POST,instance=p)
        if form_instance.is_valid():
            form_instance.save()
            return redirect('shop:categories')
        else:
            return render(request,'stock.html',{'form':form_instance})

    def get(self,request,i):
        p=Product.objects.get(id=i)
        form_instance=Stockform(instance=p)
        context={'form':form_instance}
        return render(request,'stock.html',context)
