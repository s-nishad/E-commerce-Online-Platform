from django.contrib import admin
from .models import Category, Product, Stock


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('guid', 'name', 'description')
    search_fields = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('guid', 'product_name', 'description', 'price', 'total_stock', 'get_categories')
    search_fields = ('product_name',)
    list_filter = ('categories',)
    readonly_fields = ['total_stock']

    def get_categories(self, obj):
        return obj.categories.name if obj.categories else "No Category"

    get_categories.short_description = 'Category'

    def total_stock(self, obj):
        return obj.total_stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('guid', 'product', 'quantity', 'stock_type')
    list_filter = ('stock_type', 'product')
    search_fields = ('product__product_name',)

    def save_model(self, request, obj, form, change):
        if obj.stock_type == 'OUT' and obj.product and obj.product.total_stock < obj.quantity:
            self.message_user(request, "Insufficient stock to fulfill this 'OUT' transaction.", level='error')
            return
        super().save_model(request, obj, form, change)
