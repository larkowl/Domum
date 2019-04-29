from django.contrib import admin
from .models import Announcement, Person, District, StreetType, RealType, MetroStation

admin.site.register(Announcement)
admin.site.register(Person)
admin.site.register(District)
admin.site.register(StreetType)
admin.site.register(RealType)
admin.site.register(MetroStation)
