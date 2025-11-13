
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from shop.models import Category,Product

class Signupform(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2','first_name','last_name']

class Loginform(forms.Form):
    username=forms.CharField(max_length=30)
    password=forms.CharField(widget=forms.PasswordInput)

class Categoryform(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'

class Productform(forms.ModelForm):
    class Meta:
        model=Product
        fields=['name','description','price','stock','category','image']

class Stockform(forms.ModelForm):
    class Meta:
        model=Product
        fields=['stock']