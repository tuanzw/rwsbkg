from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser

from ..validators import defaut_date, validate_alphanumeric, validate_po



class Slot(models.Model):
    bkg_date = models.DateField(default=defaut_date)
    dock_no = models.PositiveSmallIntegerField()
    s1 = models.BigIntegerField(default=0, help_text='6:00-7:00')
    s2 = models.BigIntegerField(default=0, help_text='7:00-8:00')
    s3 = models.BigIntegerField(default=0, help_text='8:00-9:00')
    s4 = models.BigIntegerField(default=0, help_text='9:00-10:00')
    s5 = models.BigIntegerField(default=0, help_text='10:00-11:00')
    s6 = models.BigIntegerField(default=0, help_text='11:00-12:00')
    s7 = models.BigIntegerField(default=0, help_text='13:00-14:00')
    s8 = models.BigIntegerField(default=0, help_text='14:00-15:00')
    s9 = models.BigIntegerField(default=0, help_text='15:00-16:00')
    s10 = models.BigIntegerField(default=0, help_text='16:00-17:00')
    s11 = models.BigIntegerField(default=0, help_text='17:00-18:00')
    s12 = models.BigIntegerField(default=0, help_text='18:00-19:00')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['bkg_date', 'dock_no'], name='unique_date_dock')] 
    
    def __str__(self) -> str:
        return f'Slot: {self.id}_{self.bkg_date}_{self.dock_no}'

class Carrier(models.Model):
    carrier = models.CharField(unique=True, max_length=30, validators=[validate_alphanumeric])
    name = models.CharField(max_length=200)
    active = models.BooleanField(default=True)
    address = models.CharField(max_length=300)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'Carrier: {self.id}_{self.carrier}'


class Driver(models.Model):
    fullname = models.CharField(max_length=100)
    idcard = models.CharField(max_length=50)
    license_valid_date = models.DateField()
    active = models.BooleanField(default=True)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name='drivers')
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['idcard', 'carrier'], name='unique_driver_carrier')]

    def __str__(self):
        return f'{self.fullname}_{self.idcard}'

class User(AbstractUser):
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name='users', null=True, blank=True)


class Vehicle(models.Model):
        
    class VehicleType(models.TextChoices):
        TRUCK1_5 = '1.5T', '1.5 Ton'
        TRUCK2_5 = '2.5T', '2.5 Ton'
        TRUCK5_0 = '5.0T', '5 Ton'
        TRUCK10 = '10T', '10 Ton'
        CONT20 = '20FT', '20 Feet'
        CONT40 = '40FT', '40 Feet'
        OTHER = 'OTHR', 'Other'
          
    registration_plate = models.CharField(unique=True, max_length=10, validators=[validate_alphanumeric])
    vehicle_type = models.CharField(max_length=4, choices=VehicleType.choices)
    active = models.BooleanField(default=True)
    valid_until = models.DateField()
    max_weight = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0,'Please input valid weight')])
    max_cbm = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0,'Please input valid cbm')])
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name='vehicles')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'Vehicle: {self.registration_plate}'
    
    class Meta:
        constraints = [models.UniqueConstraint(fields=['registration_plate', 'carrier'], name='unique_vehicle_carrier')]
    
    
class Order(models.Model):
    class OrderStatus(models.IntegerChoices):
        OPEN = 1, 'Open'
        CLOSED = 6, 'Closed'
        CANCELLED = 7, 'Cancelled'
        
    po = models.CharField(max_length=30, validators=[validate_po])
    cbm = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01,'Must be greater than 0cbm!')])
    no_of_carton = models.PositiveSmallIntegerField(default=1)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name='orders')
    status = models.PositiveSmallIntegerField(default=1, choices=OrderStatus.choices)
    valid_from = models.DateField(default=defaut_date)
    valid_until = models.DateField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'Order: {self.po}'
    

class Booking(models.Model):
    class BookingStatus(models.IntegerChoices):
        OPEN = 1, 'Open'
        CONFIRMED = 2, 'Booking Confirmed'
        READY = 3, 'Ready to Load/UnLoad'
        INPROGRESS = 4, 'Loading/Unloading'
        COMPLETED = 5, 'Completed Loading/Unloading'
        CLOSED = 6, 'Closed'
        CANCELLED = 7, 'Cancelled'
        
    class DockChoice(models.IntegerChoices):
        DOCK1 = 1, 'Dock No.1'
        DOCK2 = 2, 'Dock No.2'
        DOCK3 = 3, 'Dock No.3'
        DOCK4 = 4, 'Dock No.4'
        DOCK5 = 5, 'Dock No.5'
        
    bkg_date = models.DateField(default=defaut_date)
    status = models.PositiveSmallIntegerField(default=1, choices=BookingStatus.choices)
    cbm = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01,'Must be greater than 0cbm!'), MaxValueValidator(100,'Must be less than 100cbm!')])
    booked_slot = models.PositiveSmallIntegerField()
    actual_slot = models.PositiveSmallIntegerField()
    auto_assigned_dock = models.PositiveSmallIntegerField()
    actual_dock = models.PositiveSmallIntegerField(choices=DockChoice.choices)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='bookings')
    orders = models.ManyToManyField(Order, through='BookingOrder')
    driver = models.BigIntegerField(default=1, validators=[MinValueValidator(0, 'Not valid driver_id')])
    no_of_carton = models.PositiveSmallIntegerField(default=1)
    notes = models.CharField(max_length=300)  
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    
class BookingOrder(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    no_of_carton = models.PositiveSmallIntegerField(default=1)
    cbm = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01,'Must be greater than 0cbm!')])
    notes = models.CharField(max_length=300)



class SlotTime(models.Model):
    name=models.CharField(max_length=11)