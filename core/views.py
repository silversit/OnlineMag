from django.shortcuts import render
from products.models import Product
from .models import ThemeSetting
# Create your views here.


def homepage(request):
    promoted_products = Product.objects.filter(is_promoted=True)
    top_products = Product.objects.order_by('-quantity')[:5] # dam tova e samo za test :) nee ok taka :D nqma vreme za logikata koqto iskah
    theme = ThemeSetting.objects.first() # nok :D
    return render( request,'core/homepage.html',{
        'promoted': promoted_products,
        'top_products': top_products,
        'theme': theme.current_theme if theme else ' dark'
    })