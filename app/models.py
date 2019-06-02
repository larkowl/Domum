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
    phone = models.CharField(max_length=20)


class Announcement(models.Model):
    price = models.IntegerField(default=20000, help_text="Укажите цену в долларах США")
    district = models.ForeignKey(District, on_delete=models.CASCADE, default=0)
    distance_to_metro = models.IntegerField(default=300, help_text="Укажите расстояние в метрах")
    area = models.IntegerField(default=40, help_text="Укажите площадь в квадратных метрах")
    repairs = models.IntegerField(default=3, choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')],
                                  help_text="Оцените уровень ремонта по шкале от 0 до 5")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    comment = models.TextField(default='', help_text="Добавьте комментарий о квартире")

    def __str__(self):
        return str(self.district.name + ' - ' + str(self.area) + ' кв.м.')

    def get_absolute_url(self):
        return reverse('announcement_view', args=[str(self.id)])
