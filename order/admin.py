from django.contrib import admin

from order.models import Order
#
#
# class OrderItemInLine(admin.TabularInline):
#     model = Order
#     fields = ['product', 'quantity', 'price']
#     readonly_fields = ['product', 'quantity', 'price']
#     extra = 0
#
#     def products(self, instance):
#         return instance.order_items
#
#     def quantity(self, instance):
#         return instance.order_items.quantity
#
#     def price(self, instance):
#         return instance.order_items.price
#
#
# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     inlines = [OrderItemInLine]
#     exclude = ['items']
#     list_display = ('id', 'user', 'status', ' created_at', 'total')
#
#

admin.site.register(Order)
