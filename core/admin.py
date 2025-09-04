from django.contrib import admin
from .models import Hostel, HostelImage, Review, Amenity

@admin.register(Hostel)
class HostelAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'pricing', 'available_vacants', 'average_rating')
    search_fields = ('name', 'address')
    filter_horizontal = ('amenities',)

@admin.register(HostelImage)
class HostelImageAdmin(admin.ModelAdmin):
    list_display = ('hostel', 'image')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('hostel', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)
