from django.contrib import admin

# Register your models here.

# Car Management
from django.contrib import admin
from .forms import CarsForm
from .models import Cars, Customers, Bookings, Additions

@admin.register(Cars)
class CarsAdmin(admin.ModelAdmin):
    form = CarsForm
    list_display = ('reg_no', 'make', 'model', 'year', 'price_day', 'car_status', 'car_photo')
    search_fields = ('reg_no', 'make', 'model', 'year')
    list_filter = ('car_status',)


@admin.register(Customers)
class CustomersAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'contact', 'email')
    search_fields = ('first_name', 'last_name', 'email')
    list_filter = ('first_name', 'last_name')
    ordering = ('id',)

@admin.register(Bookings)
class BookingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'car', 'customer', 'start_da', 'end_da', 'total')
    search_fields = ('customer__first_name', 'customer__last_name', 'car__make', 'car__model')
    list_filter = ('start_da', 'end_da')
    ordering = ('-start_da',)

@admin.register(Additions)
class AdditionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price')
    search_fields = ('name',)
    ordering = ('id',)
