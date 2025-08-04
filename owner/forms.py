
from django import forms
from products.models import Product
from .models import HomepageContent

class PromotionToggleForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['is_promoted']

class HomepageContentForm(forms.ModelForm):
    class Meta:
        model = HomepageContent
        fields = ['description']

from django import forms
from .models import TransportSettings

class TransportSettingsForm(forms.ModelForm):
    class Meta:
        model = TransportSettings
        fields = ['threshold', 'fee']
