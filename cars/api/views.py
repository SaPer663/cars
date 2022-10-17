from django_filters.rest_framework import DjangoFilterBackend
from orders.models import CarModel, Color, Manufacturer, Order
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.custom_filters import CategoryFilter
from api.serializers import (AmountCarColorSerializer,
                             AmountCarManufacturerSerializer,
                             CarModelSerializer, ColorSerializer,
                             ManufacturerSerializer, OrderSerializer)


class ColorViewSet(ModelViewSet):
    """Представление модели цветов автомобиля."""
    serializer_class = ColorSerializer
    queryset = Color.objects.all()

    @action(detail=False,)
    def amount(self, request):
        """
        Возвращает список цветов с указанием количества
        заказанных авто каждого цвета.
        """
        colors = self.get_queryset()
        serializer = AmountCarColorSerializer(
            instance=colors, many=True, context={'request': request}
        )
        return Response(serializer.data)


class ManufacturerViewSet(ModelViewSet):
    """Представление модели производитель автомобиля."""
    serializer_class = ManufacturerSerializer
    queryset = Manufacturer.objects.all()

    @action(detail=False,)
    def amount(self, request):
        """
        Возвращает список производителей с указанием количества
        заказанных авто каждой марки.
        """
        manufacturers = self.get_queryset()
        serializer = AmountCarManufacturerSerializer(
            instance=manufacturers, many=True, context={'request': request}
        )
        return Response(serializer.data)


class CarModelViewSet(ModelViewSet):
    """Представление модели производитель автомобиля."""
    serializer_class = CarModelSerializer
    queryset = CarModel.objects.all()


class OrderViewSet(ModelViewSet):
    """Представление модели заказ автомобиля."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_class = CategoryFilter
    filterset_fields = ('manufacturer',)
    ordering_fields = ('amount',)
