from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('rooms/', views.room_list, name='rooms'),
    path('room/add/', views.add_room, name='add_room'),
    path('room/update/<int:pk>/', views.update_room, name='update_room'),
    path('room/delete/<int:pk>/', views.delete_room, name='delete_room'),
    path('booking/checkin/<int:pk>/', views.check_in, name='check_in'),
    path('booking/checkout/<int:pk>/', views.check_out, name='check_out'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('customer/book/<int:room_id>/', views.book_room, name='book_room'),
]

