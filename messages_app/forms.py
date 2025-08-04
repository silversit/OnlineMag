from django import  forms
from .models import Message, MessageReason

class MessageForm(forms.ModelForm):
    reasons= forms.ModelMultipleChoiceField(
        queryset=MessageReason.objects.all(),
        widget=forms.SelectMultiple,
        required=True,
        label='Why are you contacting us ?'
    )
    class Meta:
        model=Message
        fields = ['subject','content','reasons']
        widgets = {
            'reasons': forms.SelectMultiple(attrs={
                'class': 'form-select',
                'size': 4
            }),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class':'form-control'}),
        }