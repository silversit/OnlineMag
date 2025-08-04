from django.contrib import admin
from.models import Product,Promotion

# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name','price','quantity','is_promoted','created_at')
    list_filter = ('is_promoted','created_at')
    search_fields = ('name','description')
    ordering = ('-created_at',)

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('product','discount_percentage','start_date','end_date')
    list_filter = ('start_date','end_date')