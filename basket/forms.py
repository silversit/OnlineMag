from django import forms
from .models import BasketItem

class AddToBasketForm(forms.ModelForm):
    class Meta:
        model = BasketItem
        fields = ['quantity']

    def __init__(self, *args,**kwargs):
        self.product = kwargs.pop('product', None)
        super().__init__(*args,**kwargs)


    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is None or quantity < 1 :
            raise forms.ValidationError("Quantity must be at least 1.")
        if self.product:
            if quantity > self.product.quantity:
                raise forms.ValidationError(
                    f"Only {self.product.quantity} items are available in stock"
                )
        return quantity