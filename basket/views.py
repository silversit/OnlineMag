from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import BasketItem,Order,OrderItem
from.forms import AddToBasketForm
import stripe
from owner.models import TransportSettings

# Create your views here.
def get_transport_fee(request,total):
    settings = TransportSettings.objects.first()
    if not settings:
        return 0
    if total< settings.threshold:
        return settings.fee
    return 0

@login_required
def add_to_basket(request,product_id):
    product = get_object_or_404(Product,id=product_id)

    form = AddToBasketForm(request.POST,product=product)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        item,created = BasketItem.objects.get_or_create(user=request.user,product=product)
        item.quantity = quantity
        item.save()
        return  redirect('basket-view')

@login_required
def view_basket(request):
    items = BasketItem.objects.filter(user=request.user)
    if not items.exists():
        return render(
            request, 'basket/view_basket.html',
            {
                'items':[],
                'total':0,
                'transport_fee':0,
                'grand_total':0,

            }
        )

    total = sum(item.total_price() for item in items)
    transport_fee = get_transport_fee(request,total)
    grand_total = total + transport_fee

    return render(
        request,'basket/view_basket.html',{
        'items':items,
        'total':total,
        'transport_fee':transport_fee,
        'grand_total':grand_total,
    }
    )

@login_required
def remove_from_basket(request,item_id):
    item = get_object_or_404(BasketItem, id=item_id,user=request.user)
    item.delete()
    return redirect('basket-view')


@login_required
def checkout(request):
    items = BasketItem.objects.filter(user=request.user)
    if not items:
        return redirect('basket-view')
    total = sum(item.total_price() for item in items)
    transport_fee = get_transport_fee(request,total)
    grand_total = total + transport_fee

    order = Order.objects.create(user=request.user,transport_fee=transport_fee)
    line_items = []

    for item in items:
        OrderItem.objects.create(order=order,product=items.product,quantity=item.quantity)
        line_items.append(
            { 'price_data':{
            'currency':'usd',
            'product_data':{'name':item.product.name},
            'unit_amount':int(item.product.price*100)
        },
            'quantity':item.quantity,}

        )
    if transport_fee > 0:
      line_items.append(  {'price_data': {
            'currency': 'usd',
            'product_data': {'name': 'Transport Fee'},
            'unit_amount': int(item.product.price * 100)
        },
            'quantity': 1, }

    )

    items.delete()

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/basket/checkout/success/'),
        cancel_url=request.build_absolute_uri('/basket/'),
    )
    return redirect(session.url,code=303)


@login_required
def payment_success(request):
    order = Order.objects.filter(user=request.user).latest('created_at')

    if order.status != 'paid':
        order.status = 'paid'
        order.save()
        for item in order.orderitems_set.all():
            product = item.product
            if product.quantity >= item.quantity:
                product.quantity -= item.quantity
                product.save(
                )

    return render(
        request,
        'basket/checkout.html',
        {
            'order':order,
            'transport_fee': order.transport_fee
        }
    )
