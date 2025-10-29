from django.shortcuts import render
from django.views import View
from shop.models import Category
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