from django.urls import reverse
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
import os


class District(models.Model):
    name = models.CharField(max_length=30)
    pseudo_id = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    ava = models.ImageField(null=True, blank=True, upload_to='images/avas/')
    phone = models.CharField(max_length=20, null=True, blank=True)

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.ava.path):
            os.remove(self.ava.path)
        super(Person, self).delete(*args, **kwargs)


class OrderId(models.Model):
    order_id = models.IntegerField(default=30)

    def next(self):
        self.order_id += 1
        self.save()
        return 'order_id_' + str(self.order_id - 1)


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
    metro_id = models.IntegerField(default=0)
    floor = models.IntegerField(default=1, help_text="Укажите номер этажа")
    rooms_number = models.IntegerField(default=1, help_text="Укажите количество комнат")
    beds = models.IntegerField(default=1, help_text="Укажите количество спальных мест")
    furniture = models.BooleanField(default=False)
    garage = models.BooleanField(default=False)

    street = models.CharField(max_length=30, default='', help_text="Укажите название улицы")
    home_number = models.CharField(max_length=5, default='1', help_text="Укажите номер дома")
    date = models.DateField(default=timezone.now)
    comment = models.TextField(default='', help_text="Добавьте комментарий о квартире", null=True, blank=True)

    img_path = 'images/announcements/'

    photo1 = models.ImageField(null=True, blank=True, upload_to=img_path)
    photo2 = models.ImageField(null=True, blank=True, upload_to=img_path)
    photo3 = models.ImageField(null=True, blank=True, upload_to=img_path)
    photo4 = models.ImageField(null=True, blank=True, upload_to=img_path)
    photo5 = models.ImageField(null=True, blank=True, upload_to=img_path)
    photo6 = models.ImageField(null=True, blank=True, upload_to=img_path)
    photo7 = models.ImageField(null=True, blank=True, upload_to=img_path)
    photo8 = models.ImageField(null=True, blank=True, upload_to=img_path)

    def __str__(self):
        return str(self.district.name + ' - ' + str(self.area) + ' кв.м.')

    def get_absolute_url(self):
        return reverse('announcement_view', args=[str(self.id)])

    def form_rate(self, transform=True, need_round=True, feedbacks=None):
        if feedbacks is None:
            feedbacks = self.find_feedbacks()
        av_rate = -1
        if len(feedbacks) > 0:
            av_value = 0
            for i in feedbacks:
                av_value += i.rate
            av_value /= len(feedbacks)
            if need_round:
                av_value = round(av_value, 1)
            if int(av_value) == av_value:
                av_value = int(av_value)
            av_rate = av_value
        if transform:
            if av_rate == -1:
                av_rate = 'Нема оцінки'
            else:
                av_rate = 'Бал: ' + str(av_rate) + ' / 10'
        return av_rate

    def find_feedbacks(self):
        return Feedback.objects.filter(deal__announcement__pk=self.pk)

    def occupied_dates(self):
        data = Deal.objects.filter(announcement__pk=self.pk)
        result = []
        for i in data:
            result.append(i.term)
        if len(result) == 0:
            return ''
        return ' '.join(result)


class Deal(models.Model):
    buyer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    term = models.TextField()
    price = models.IntegerField(default=0)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, default=0)


class Feedback(models.Model):
    deal = models.OneToOneField(Deal, on_delete=models.CASCADE, default=0)
    rate = models.FloatField()
    text = models.TextField()
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.id)
