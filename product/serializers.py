from rest_framework import serializers
from product.models import Product


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'price')



class ProductDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'title', 'description', 'price', 'image')

class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def validated_price(self, price):
        if price < 0:
            raise serializers.ValidationError('Цена не может быть отрицательной')
        return price

    # def validate(self):