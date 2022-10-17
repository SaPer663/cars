from django.contrib import admin
from orders.models import Color, Manufacturer, CarModel, Order


admin.site.register(Color)
admin.site.register(CarModel)
admin.site.register(Manufacturer)
admin.site.register(Order)
