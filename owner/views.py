from django.shortcuts import render
import  csv
from  datetime import timedelta
from django.contrib.auth.mixins import  LoginRequiredMixin
from django.db.models import Count,Sum,ExpressionWrapper,F,FloatField
from django.db.models.functions import TruncDate
from django.http import  HttpResponse,HttpResponseForbidden
from django.shortcuts import redirect,get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views import View
from django.views.generic.edit import UpdateView,DeleteView
from products.models import  Product
from messages_app.models import Message
from products.forms import ProductForm
from django.core.exceptions import PermissionDenied
from owner.forms import  HomepageContentForm
from owner.models import HomepageContent
from .models import TransportSettings
from .forms import TransportSettingsForm

from basket.models import Order, OrderItem

from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

from messages_app.models import MessageReply
from .decorators import owner_required
# Create your views here.
@method_decorator(owner_required, name='dispatch')
class OwnerDashboardView(View):
    def get(self, request):
        low_stock_products = Product.objects.filter(quantity__lt=10)
        return render(request, 'owner/dashboard.html', {
            'low_stock_products': low_stock_products
        })

    def post(self, request):
        product_id = request.POST.get("product_id")
        additional_qty = request.POST.get("additional_qty")

        if product_id and additional_qty:
            product = get_object_or_404(Product, pk=product_id)
            try:
                qty = int(additional_qty)
                product.quantity += qty
                product.save()
            except ValueError:
                pass  # Optionally show a warning message

        return redirect('owner-dashboard')

# --- Product Views ---
@method_decorator(owner_required, name='dispatch')
class OwnerProductListView(View):
    def get(self, request):
        products = Product.objects.all().order_by('-id')
        return render(request, 'owner/product_list.html', {'products': products})
class OwnerReplyMessageView(LoginRequiredMixin, View):
    def post(self, request, message_id):
        if not request.user.is_authenticated or request.user.role != 'owner':
            return HttpResponseForbidden()

        message = get_object_or_404(Message, id=message_id)
        reply_content = request.POST.get("reply", "").strip()

        if reply_content:
            # Create a new reply in the thread
            MessageReply.objects.create(
                message=message,
                sender=request.user,
                content=reply_content
            )

            # Update message status and flags
            message.status = "answered"
            message.recipient = message.sender
            message.answered = True
            message.updated = False  # ✅ This sends it back to the user and removes from "updated"
            message.save()

        return redirect("owner-messages")

@method_decorator(owner_required, name='dispatch')
class OwnerProductCreateView(View):
    def get(self, request):
        form = ProductForm()
        return render(request, 'owner/product_form.html', {'form': form})

    def post(self, request):
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('owner-product-list')
        return render(request, 'owner/product_form.html', {'form': form})


@method_decorator(owner_required, name='dispatch')
class OwnerProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'owner/product_form.html'
    success_url = '/owner/products/'


@method_decorator(owner_required, name='dispatch')
class OwnerProductDeleteView(DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'  # ← reuse here
    success_url = reverse_lazy('owner-product-list')


# --- Message Center ---
@method_decorator(owner_required, name='dispatch')
class OwnerMessageCenterView(View):
    def get(self, request):
        answered = Message.objects.filter(answered=True, updated=False)
        updated = Message.objects.filter(answered=True, updated=True)
        new_msgs = Message.objects.filter(answered=False)

        return render(request, 'owner/messages.html', {
            'answered': answered,
            'updated': updated,
            'new': new_msgs
        })

@method_decorator(owner_required, name='dispatch')
class PromotionToggleView(View):
    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_promoted = not product.is_promoted
        product.save()
        return redirect('owner-product-list')

@method_decorator(owner_required, name='dispatch')
class HomepageEditView(View):
    def get(self, request):
        content, _ = HomepageContent.objects.get_or_create(pk=1)
        form = HomepageContentForm(instance=content)
        return render(request, 'owner/homepage_edit.html', {'form': form})

    def post(self, request):
        content, _ = HomepageContent.objects.get_or_create(pk=1)
        form = HomepageContentForm(request.POST, instance=content)
        if form.is_valid():
            form.save()
            return redirect('owner-dashboard')
        return render(request, 'owner/homepage_edit.html', {'form': form})




User = get_user_model()

@method_decorator(owner_required, name='dispatch')
class OwnerUserListView(View):
    def get(self, request):
        users = User.objects.exclude(role__in=['admin', 'owner']).order_by('-date_joined')
        return render(request, 'owner/user_list.html', {'users': users})


@method_decorator(owner_required, name='dispatch')
@method_decorator(require_POST, name='dispatch')
class OwnerBlockUserView(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.is_active = not user.is_active
        user.save()
        return redirect('owner-user-list')


@method_decorator(owner_required, name='dispatch')
@method_decorator(require_POST, name='dispatch')
class OwnerDeleteUserView(View):
    def post(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        return redirect('owner-user-list')











@method_decorator(owner_required, name='dispatch')
class TransportSettingsView(View):
    def get(self, request):
        settings, _ = TransportSettings.objects.get_or_create(pk=1)
        form = TransportSettingsForm(instance=settings)
        return render(request, 'owner/transport_settings.html', {'form': form})

    def post(self, request):
        settings, _ = TransportSettings.objects.get_or_create(pk=1)
        form = TransportSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            return redirect('owner-dashboard')
        return render(request, 'owner/transport_settings.html', {'form': form})







ORDER_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('in_transport', 'In Transport'),
    ('completed', 'Completed'),
    ('cancelled', 'Cancelled'),
    ('refund_requested', 'Refund Requested'),
    ('refunded', 'Refunded'),
    ('awaiting_quantity', 'Awaiting Quantity'),
]


@method_decorator(owner_required, name='dispatch')
class UpdateOrderStatusView(View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get("status")
        if new_status in dict(ORDER_STATUS_CHOICES).keys():
            order.status = new_status
            order.save()
        return redirect('owner-order-list')




@method_decorator(owner_required, name='dispatch')
class OwnerOrderListView(View):
    def get(self, request):
        status_filter = request.GET.get("status")
        if status_filter:
            orders = Order.objects.filter(status=status_filter).order_by("-created_at")
        else:
            orders = Order.objects.all().order_by("-created_at")

        return render(request, 'owner/order_list.html', {
            'orders': orders,
            'statuses': ORDER_STATUS_CHOICES,
            'selected_status': status_filter
        })

@method_decorator(owner_required, name='dispatch')
class OwnerUpdateOrderStatusView(View):
    def post(self, request, order_id):
        order = get_object_or_404(Order, pk=order_id)
        new_status = request.POST.get("status")
        if new_status in dict(ORDER_STATUS_CHOICES):
            order.status = new_status
            order.save()
        return redirect('owner-order-list')

@method_decorator(owner_required, name='dispatch')
class ExportOrdersCSVView(View):
    def get(self, request):
        # Filtered or all orders
        status_filter = request.GET.get("status")
        if status_filter:
            orders = Order.objects.filter(status=status_filter).order_by("-created_at")
        else:
            orders = Order.objects.all().order_by("-created_at")

        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="orders_export.csv"'

        writer = csv.writer(response)
        writer.writerow([
            "Order ID", "User", "Created At", "Status",
            "Total Amount", "Transport Fee", "Total Items", "Payment Status"
        ])

        for order in orders:
            writer.writerow([
                order.id,
                order.user.username if order.user else "Guest",
                order.created_at.strftime("%Y-%m-%d %H:%M"),
                order.status,
                f"{order.total_price:.2f}",
                f"{order.transport_fee:.2f}" if hasattr(order, "transport_fee") else "0.00",
                order.items.count(),
                "Paid" if order.status == "paid" else "Unpaid"
            ])

        return response
@method_decorator(owner_required, name='dispatch')
class StatisticsView(View):
    def get(self, request):
        all_orders = Order.objects.all()

        # Total income from line totals in paid or completed orders
        income = 0
        if OrderItem.objects.filter(order__status__in=["paid", "completed"]).exists():
            income = (
                OrderItem.objects
                .filter(order__status__in=["paid", "completed"])
                .annotate(
                    line_total=ExpressionWrapper(
                        F("quantity") * F("product__price"),
                        output_field=FloatField()
                    )
                )
                .aggregate(total=Sum("line_total"))["total"] or 0
            )

        # Transport fee income from all orders
        transport_income = all_orders.aggregate(total=Sum("transport_fee"))["total"] or 0

        # Count of orders by status
        order_counts = all_orders.values("status").annotate(count=Count("id"))

        # Daily orders summary (past 7 days)
        last_7_days = now() - timedelta(days=7)
        daily_orders = []
        if all_orders.filter(created_at__gte=last_7_days).exists():
            daily_orders = (
                all_orders
                .filter(created_at__gte=last_7_days)
                .annotate(day=TruncDate("created_at"))
                .values('day')
                .annotate(
                    count=Count('id'),
                    total=Sum(
                        ExpressionWrapper(
                            F("items__quantity") * F("items__product__price"),
                            output_field=FloatField()
                        )
                    )
                )
                .order_by('day')
            )

        return render(request, "owner/statistics.html", {
            "total_income": round(income, 2),
            "transport_income": round(transport_income, 2),
            "order_counts": order_counts,
            "daily_orders": daily_orders,
        })