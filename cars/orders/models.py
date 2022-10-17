from datetime import date

from django.db import models


class Color(models.Model):
    name = models.CharField(
        'название цвета',
        max_length=64
    )

    class Meta:
        verbose_name = 'Цвет'
        verbose_name_plural = 'Цвета'

    def __str__(self):
        return self.name


class Manufacturer(models.Model):
    name = models.CharField(
        'Название марки',
        max_length=128,
        unique=True
    )

    class Meta:
        verbose_name = 'Марка'
        verbose_name_plural = 'Марки'

    def __str__(self):
        return self.name


class CarModel(models.Model):
    name = models.CharField(
        'Название модели',
        max_length=128
    )
    manufacturer = models.ForeignKey(
        Manufacturer, on_delete=models.CASCADE,
        related_name='car_models',
        verbose_name='Марка'
    )

    class Meta:
        verbose_name = 'Модель'
        verbose_name_plural = 'Модель'

    def __str__(self):
        return f'{self.manufacturer.name} {self.name}'


class Order(models.Model):
    color = models.ForeignKey(
        Color,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name='Цвет',
    )
    model = models.ForeignKey(
        CarModel,
        on_delete=models.CASCADE,
        related_name="orders",
        verbose_name='Модель',
    )
    amount = models.PositiveSmallIntegerField()
    order_date = models.DateField(
        'Дата заказа',
        default=date.today,
        db_index=True
    )

    class Meta:
        ordering = ('amount',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'{self.model.name} {self.color.name} {self.order_date}'
