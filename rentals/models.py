# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

# Cars Module
class Cars(models.Model):
    id = models.BigAutoField(primary_key=True)
    reg_no = models.CharField(unique=True, max_length=10)
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.IntegerField()
    price_day = models.DecimalField(max_digits=10, decimal_places=2)
    car_status = models.CharField(max_length=11)
    car_photo = models.ImageField(upload_to='car_photos/', blank=True, null=True)

    class Meta:
        db_table = 'cars'
       


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
        managed = False


#Additions Module
class Additions(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'additions'
        managed = False

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
        managed = False
      
    

    

