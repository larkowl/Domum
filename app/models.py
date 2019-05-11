from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings


class District(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)


class StreetType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class RealType(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class MetroStation(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Announcement(models.Model):
    real_type = models.ForeignKey(RealType, on_delete=models.CASCADE, default=0)
    district = models.ForeignKey(District, on_delete=models.CASCADE, default=0)
    street_type = models.ForeignKey(StreetType, on_delete=models.CASCADE, default=0)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    station = models.ForeignKey(MetroStation, on_delete=models.CASCADE, default=0)

    price = models.IntegerField(default=20000, help_text="Укажите цену в долларах США")
    distance_to_metro = models.IntegerField(default=300, help_text="Укажите расстояние в метрах")
    area = models.IntegerField(default=40, help_text="Укажите площадь в квадратных метрах")
    repairs = models.IntegerField(default=3, choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
                                  help_text="Оцените уровень ремонта по шкале от 0 до 5")
    floor = models.IntegerField(default=1, help_text="Укажите номер этажа")
    rooms_number = models.IntegerField(default=1, help_text="Укажите количество комнат")
    beds = models.IntegerField(default=1, help_text="Укажите количество спальных мест")
    furniture = models.BooleanField(default=False)
    garage = models.BooleanField(default=False)

    street = models.CharField(max_length=30, default='', help_text="Укажите название улицы")
    home_number = models.CharField(max_length=5, default='1', help_text="Укажите номер дома")
    date = models.DateField(default=timezone.now)
    comment = models.TextField(default='', help_text="Добавьте комментарий о квартире")

    def __str__(self):
        return str(self.district.name + ' - ' + str(self.area) + ' кв.м.')

    def get_absolute_url(self):
        return reverse('announcement_view', args=[str(self.id)])
