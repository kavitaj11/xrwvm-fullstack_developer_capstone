from django.contrib import admin
from .models import CarMake, CarModel

# Inline class for CarModel to be displayed within CarMake admin
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1

# Admin class for CarMake with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    list_display = ('name', 'country', 'founded_year')
    search_fields = ['name', 'country']

# Admin class for CarModel
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'car_make', 'type', 'year', 'dealer_id')
    list_filter = ('car_make', 'type', 'year')
    search_fields = ['name', 'car_make__name']

# Register models here
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)