# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from cloudinary.models import CloudinaryField
from datetime import datetime, date
from zoneinfo import ZoneInfo

# Cars Module
class Cars(models.Model):
    id = models.BigAutoField(primary_key=True)
    reg_no = models.CharField(unique=True, max_length=10)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    price_day = models.DecimalField(max_digits=10, decimal_places=2)
    car_status = models.CharField(max_length=11)
    car_photo = CloudinaryField('car_photo', blank=True, null=True)

    class Meta:
        db_table = 'cars'
        

    def __str__(self):
        return f"{self.make} {self.model} ({self.reg_no})"

    def get_daily_price(self, rental_days, check_date=None):
        if check_date is None:
            # Barbados timezone
            check_date = datetime.now(ZoneInfo("America/Barbados")).date()

        current_season_price = None
        for sp in self.season_prices.select_related('season').all():
            season = sp.season
            if season.start_date <= check_date <= season.end_date:
                current_season_price = sp
                break

        # fallback to base price if no active season found
        if not current_season_price:
            return self.price_day

        if rental_days <= 2:
            return current_season_price.price_1_2_days
        elif rental_days <= 4:
            return current_season_price.price_3_4_days
        elif rental_days <= 6:
            return current_season_price.price_5_6_days
        else:
            return current_season_price.price_7_plus_days
    
    def get_weekly_display_price(self, check_date=None):
        """Returns the 7+ day price based on season."""
        price = self.get_daily_price(rental_days=7, check_date=check_date)
        return f"{price:.0f}"



# Customers Module
class Customers(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email = models.CharField(unique=True, max_length=255)
    license_photo = models.ImageField(blank=True, null=True)

    class Meta:
        db_table = 'customers'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
        


#Additions Module
class Additions(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'additions'

    def __str__(self):
        return self.name

        

# Bookings Module
class Bookings(models.Model):
    id = models.BigAutoField(primary_key=True)
    car = models.ForeignKey('Cars', on_delete=models.CASCADE, blank=True, null=True)
    customer = models.ForeignKey('Customers', on_delete=models.CASCADE, blank=True, null=True)
    start_da = models.DateField()
    start_time = models.TimeField()
    end_da = models.DateField()
    end_time = models.TimeField(null=True)
    pickup_loc = models.CharField(max_length=255)
    additions = models.ManyToManyField(Additions, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'bookings'

    def __str__(self):
        return f"Booking #{self.id} - {self.car} ({self.start_da} → {self.end_da})"



# ===========================
# Seasonal Pricing System
# ===========================
class Season(models.Model):
    SEASON_CHOICES = [
        ('summer', 'Summer'),
        ('winter', 'Winter'),
        ('special', 'Special'),
    ]
    name = models.CharField(max_length=20, choices=SEASON_CHOICES, unique=True)
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'seasons'

    def __str__(self):
        return f"{self.get_name_display()} ({self.start_date} → {self.end_date})"

    def is_in_season(self, check_date=None):
        if check_date is None:
            check_date = datetime.now(ZoneInfo("America/Barbados")).date()
        return self.start_date <= check_date <= self.end_date
    
class SeasonDateRange(models.Model):
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='date_ranges')
    start_date = models.DateField()
    end_date = models.DateField()

    class Meta:
        db_table = 'season_date_ranges'
        ordering = ['start_date']

    def __str__(self):
        return f"{self.season.get_name_display()} ({self.start_date} → {self.end_date})"

class CarSeasonPrice(models.Model):
    car = models.ForeignKey(Cars, on_delete=models.CASCADE, related_name="season_prices")
    season = models.ForeignKey(Season, on_delete=models.CASCADE)

    price_1_2_days = models.DecimalField(max_digits=8, decimal_places=2)
    price_3_4_days = models.DecimalField(max_digits=8, decimal_places=2)
    price_5_6_days = models.DecimalField(max_digits=8, decimal_places=2)
    price_7_plus_days = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'car_season_prices'
        unique_together = ('car', 'season')

    def __str__(self):
        return f"{self.car.make} {self.car.model} - {self.season.get_name_display()}"


    
      
    

    

