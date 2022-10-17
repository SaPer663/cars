from django.http import Http404
from django.shortcuts import get_object_or_404
from orders.models import CarModel, Color, Manufacturer, Order
from rest_framework import serializers


class ColorSerializer(serializers.ModelSerializer):
    """Сериализатор модели цвет автомобиля."""

    class Meta:
        fields = '__all__'
        model = Color


class AmountCarColorSerializer(serializers.ModelSerializer):
    """
    Сериализатор представления количества автомобилей по цветам автомобиля.
    """
    amount = serializers.SerializerMethodField(
        method_name='get_amount'
    )

    class Meta:
        fields = ('name', 'amount')
        model = Color

    def get_amount(self, obj):
        """Количество заказанных автомобилей определённого цвета."""
        return obj.orders.count()


class ManufacturerSerializer(serializers.ModelSerializer):
    """Сериализатор модели производитель автомобиля."""

    class Meta:
        fields = '__all__'
        model = Manufacturer


class AmountCarManufacturerSerializer(serializers.ModelSerializer):
    """Сериализатор представления количества автомобилей по производителю."""
    amount = serializers.SerializerMethodField(
        method_name='get_amount'
    )

    class Meta:
        fields = ('name', 'amount')
        model = Manufacturer

    def get_amount(self, obj):
        """Количество заказанных автомобилей определённого производителя."""
        return Order.objects.filter(model__manufacturer=obj).count()


class CarModelSerializer(serializers.ModelSerializer):
    """Сериализатор модели модель автомобиля."""
    manufacturer = serializers.SlugRelatedField(
        queryset=Manufacturer.objects.all(),
        slug_field='name',
    )

    class Meta:
        fields = ('name', 'manufacturer')
        model = CarModel


class OrderSerializer(serializers.ModelSerializer):
    """Сериализатор модели заказ автомобиля."""
    color = serializers.SlugRelatedField(
        queryset=Color.objects.all(),
        slug_field='name',
    )
    model = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
    )
    manufacturer = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name',
        source='model.manufacturer'
    )

    class Meta:
        fields = (
            'id',
            'order_date',
            'color',
            'model',
            'manufacturer',
            'amount'
        )
        model = Order

    def validate(self, data):
        custom_data = data.copy()
        manufacturer = self.initial_data.get('manufacturer')
        model = self.initial_data.get('model')
        try:
            manufacturer = get_object_or_404(Manufacturer, name=manufacturer)
        except Http404:
            raise serializers.ValidationError(
                {'manufacturer': 'Нет такой марки автомобиля в базе.'}
            )
        try:
            model = get_object_or_404(
                CarModel, name=model, manufacturer=manufacturer
            )
        except Http404:
            raise serializers.ValidationError(
                {'model': 'Нет такой модели автомобиля в базе.'}
            )
        custom_data['model'] = model
        return super().validate(custom_data)
