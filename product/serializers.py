from django.shortcuts import get_object_or_404
from rest_framework import serializers
from .models import Category, Stock, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['guid', 'name', 'description', 'created', 'updated', 'is_active']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['guid', 'quantity', 'stock_type', 'created', 'updated', 'is_active']


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer()
    stocks = StockSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'guid', 'product_name', 'description', 'price', 'total_stock',
            'categories', 'stocks', 'created', 'updated', 'is_active'
        ]
        read_only_fields = ['total_stock']

    def create(self, validated_data):
        category_data = validated_data.pop('categories', None)
        stocks_data = validated_data.pop('stocks', [])

        # Create the Product instance
        product = Product.objects.create(**validated_data)

        # Associate the ForeignKey category
        if category_data:
            category, created = Category.objects.get_or_create(**category_data)
            product.categories = category
            product.save()

        # Create and associate stocks with the product
        for stock_data in stocks_data:
            Stock.objects.create(product=product, **stock_data)

        return product

    def update(self, instance, validated_data):
        # Extract nested data
        category_data = validated_data.pop('categories', None)
        stocks_data = validated_data.pop('stocks', [])

        # Update Product instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update the category (ForeignKey relationship)
        if category_data:
            category, created = Category.objects.get_or_create(**category_data)
            instance.categories = category
            instance.save()

        # Update stocks (related objects)
        if stocks_data:
            for stock_data in stocks_data:
                Stock.objects.update_or_create(
                    product=instance, stock_type=stock_data.get('stock_type'), defaults=stock_data
                )

        return instance


class CreateStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['guid', 'quantity', 'stock_type']

    def create(self, validated_data):
        product_guid = self.context['product_guid']
        product = Product.objects.get(guid=product_guid)

        stock = Stock.objects.create(product=product, **validated_data)
        return stock
