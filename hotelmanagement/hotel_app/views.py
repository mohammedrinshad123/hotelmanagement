from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import CustomUser, Customer, Room, Booking
from .forms import CustomUserCreationForm, RoomForm
from django.contrib.auth.forms import AuthenticationForm
from datetime import timedelta

def home_view(request):
    return render(request, 'hotel_app/home.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_customer:
                return redirect('customer_dashboard')
            elif user.is_staffuser:
                return redirect('staff_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    return render(request, 'hotel_app/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create associated customer profile
            Customer.objects.create(user=user)
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'hotel_app/register.html', {'form': form})

@login_required
def staff_dashboard(request):
    customers = Customer.objects.all()
    rooms = Room.objects.all()
    bookings = Booking.objects.all()
    return render(request, 'hotel_app/staff_dashboard.html', {
        'customers': customers,
        'rooms': rooms,
        'bookings': bookings
    })

# Room CRUD
@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('staff_dashboard')
    else:
        form = RoomForm()
    return render(request, 'hotel_app/room_form.html', {'form': form})

@login_required
def update_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    form = RoomForm(request.POST or None, instance=room)
    if form.is_valid():
        form.save()
        return redirect('staff_dashboard')
    return render(request, 'hotel_app/room_form.html', {'form': form})

@login_required
def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    room.delete()
    return redirect('staff_dashboard')

# Check-in / Check-out
@login_required
def check_in(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.is_checked_in = True
    booking.save()
    return redirect('staff_dashboard')

@login_required
def check_out(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    booking.is_checked_out = True
    booking.room.is_available = True
    booking.room.save()
    booking.save()
    return redirect('staff_dashboard')

@login_required
def customer_dashboard(request):
    # Auto-create customer profile if it does not exist
    customer_profile, created = Customer.objects.get_or_create(user=request.user)

    # Available rooms
    available_rooms = Room.objects.filter(is_available=True)

    # My bookings
    my_bookings = Booking.objects.filter(customer=customer_profile)

    return render(request, 'hotel_app/customer_dashboard.html', {
        'available_rooms': available_rooms,
        'my_bookings': my_bookings
        
    })


@login_required
def book_room(request, room_id):
    # Auto-create profile if missing
    customer_profile, created = Customer.objects.get_or_create(user=request.user)

    # Ensure the room exists and is available
    room = get_object_or_404(Room, id=room_id, is_available=True)

    # Create booking
    Booking.objects.create(customer=customer_profile, room=room)

    # Mark as unavailable
    room.is_available = False
    room.save()

    return redirect('customer_dashboard')

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'hotel_app/rooms_list.html', {'rooms': rooms})
