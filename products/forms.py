from django import forms
from .models import Product,Promotion

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields = ['name','description','image','price','quantity','is_promoted']

class PromotionForm(forms.ModelForm):
    class Meta:
        model = Promotion
        fields = ['product','discount_percentage','start_date','end_date']
