from django.contrib import admin
from .models import Monument, Booking

admin.site.register(Monument)
admin.site.register(Booking)

from .models import MonumentImage

class MonumentImageAdmin(admin.ModelAdmin):
    list_display = ['monument', 'image']

admin.site.register(MonumentImage, MonumentImageAdmin)

