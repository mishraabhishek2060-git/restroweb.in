from django.contrib import admin

from .models import ContactMessage, MenuItem, Order, OrderItem

admin.site.register(ContactMessage)


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'half_price', 'price')
    search_fields = ('name', 'description')


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('item_name', 'plate_size', 'quantity', 'unit_price', 'line_total')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'customer_phone', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('customer_name', 'customer_phone')
    readonly_fields = ('public_id', 'customer_name', 'customer_phone', 'total', 'created_at')
    inlines = (OrderItemInline,)
