from django.contrib import admin
from .models import Announcement, Person, District

admin.site.register(Announcement)
admin.site.register(Person)
admin.site.register(District)
