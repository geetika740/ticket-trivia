from django.contrib import admin
from .models import Monument, Booking, MonumentImage

# Inline images inside Monument admin
class MonumentImageInline(admin.TabularInline):
    model = MonumentImage
    extra = 1  # Allows adding one extra image entry by default
    readonly_fields = ['image']  # Makes the image field read-only for preview

# Enhanced Monument admin view
class MonumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name']
    list_filter = ['category']
    inlines = [MonumentImageInline]

# Enhanced Booking admin view
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'monument', 'visit_date', 'num_tickets']
    search_fields = ['user__username', 'monument__name']
    list_filter = ['visit_date', 'monument']

# Register updated admins
admin.site.register(Monument, MonumentAdmin)
admin.site.register(Booking, BookingAdmin)

# Still register MonumentImage for direct view
class MonumentImageAdmin(admin.ModelAdmin):
    list_display = ['monument', 'image']

admin.site.register(MonumentImage, MonumentImageAdmin)
