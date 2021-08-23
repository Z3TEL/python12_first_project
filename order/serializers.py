from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ('id', 'order')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True)
    created_at = serializers.DateTimeField(read_only=True)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Order
        exclude = ('user',)

    def create(self, validated_data):
        request = self.context.get('request')
        items = validated_data.pop('items')
        user = request.user
        order = Order.objects.create(user=user)
        for item in items:
            item = OrderItem.objects.create(order=order,
                                            product=item['product'],
                                            quantity=item['quantity'])
            order.items.add(item)
        order.save()
        return order
