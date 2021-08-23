from django import forms
from django.contrib import admin

from order.models import *


class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('status', 'user')


class OrderItemsInLine(admin.TabularInline):
    model = OrderItem



class TotalSumFilter(admin.SimpleListFilter):
    title = 'Фильтрация по сумме заказа'
    parameter_name = 'total_sum'


    def lookups(self, request, model_admin):
        return (
            ('0to50000', 'от 0 до 50000'),
            ('50000to50000', 'от 50000 до 100000'),
            ('100000to150000', 'от 100000 до 150000'),
            ('from150000', 'от 150000 и выше')
        )

    def queryset(self, request, queryset):
        if self.value() == '0to50000':
            return queryset.filter(total_sum__lte=50000)
        elif self.value() == '50000to100000':
            return queryset.filter(total_sum__range=[50000, 100000])
        elif self.value() == '100000to150000':
            return queryset.filter(total_sum__range=[100000, 150000])
        elif self.value() == '100000to150000':
            return queryset.filter(total_sum__gte=150000)
        else:
            return queryset

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemsInLine
    ]
    exclude = ('products',)
    form = OrderAdminForm
    readonly_fields = ['user', 'total', 'created_at']
    list_display = ['id', 'status', 'total', 'created_at']
    list_filter = ['status', TotalSumFilter]
    search_fields = ['products__title']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.user = request.user
        super().save_model(request, obj, form, change)

# TODO: Исправить сохранение total_sum



admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
