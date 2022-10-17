from django_filters import rest_framework as filters
from orders.models import Manufacturer, Order


class CategoryFilter(filters.FilterSet):
    manufacturer = filters.ModelChoiceFilter(
        field_name='model__manufacturer',
        queryset=Manufacturer.objects.all(),
        to_field_name='name',
    )

    class Meta:
        model = Order
        fields = ('manufacturer',)
