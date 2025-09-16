from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Customer, Room, Booking,Staff

# Custom admin for CustomUser
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'is_customer', 'is_staffuser', 'is_staff', 'is_superuser']


admin.site.register(Staff)
admin.site.register(Customer)
admin.site.register(CustomUser, CustomUserAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address']

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['room_number', 'room_type', 'is_available', 'price_per_night']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['customer', 'room', 'check_in', 'check_out', 'is_checked_in', 'is_checked_out']


