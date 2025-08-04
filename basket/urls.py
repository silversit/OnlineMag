from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_basket, name='basket-view'),
    path('add/<int:product_id>/',views.add_to_basket,name='add-to-basket'),
    path('remove/<int:item_id>/', views.remove_from_basket,name='remove-from-basket'),
    path('checkout/',views.checkout,name='checkout'),
    path('checkout/success/', views.payment_success,name='payment-success'),
]