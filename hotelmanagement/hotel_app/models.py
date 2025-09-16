from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    is_staffuser = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Staff(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"Staff: {self.user.username}"


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return f"Customer: {self.user.username}"


class Room(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
    ]
    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    is_available = models.BooleanField(default=True)
    price_per_night = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return f"Room {self.room_number} ({self.get_room_type_display()})"


class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateField(null=True, blank=True)   
    check_out = models.DateField(null=True, blank=True)  
    booking_date = models.DateTimeField(default=timezone.now)
    is_checked_in = models.BooleanField(default=False)
    is_checked_out = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.customer.user.username} - Room {self.room.room_number}"
