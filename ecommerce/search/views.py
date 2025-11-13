from django.shortcuts import render

# Create your views here.

from django.views import View
from django.db.models import Q

from shop.models import Product


class Searchview(View):
    def get(self,request):
        query = request.GET['q']
        print(query)
        if query:
             p=Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query))
             context={'products': p}
        return render(request,'search.html',context)