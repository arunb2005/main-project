"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from cart import views

from cart.views import Addtocart,Cartview

app_name='cart'

urlpatterns = [
    path('addtocart/<int:i>',views.Addtocart.as_view(),name='addtocart'),
    path('cartview',views.Cartview.as_view(),name='cartview'),
    path('addquantity/<int:i>',views.Addquantity.as_view(),name='addquantity'),
    path('deletequantity/<int:i>',views.Deletequantity.as_view(),name='deletequantity'),
    path('delete/<int:i>',views.Delete.as_view(),name='delete'),
    path('chekout',views.Checkout.as_view(),name='checkout'),
    path('payment_success/<i>',views.Payment_success.as_view(),name='payment_success'),
    path('your_order',views.Your_orders.as_view(),name='your_orders')
]
