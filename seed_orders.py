import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hotel_House.settings')
django.setup()

from django.contrib.auth.models import User
from User_Dashboard.models import Order, OrderItem, MenuItem

def seed():
    admin = User.objects.filter(username='admin').first()
    guest = User.objects.filter(username='guest_user').first()

    steak = MenuItem.objects.filter(name__icontains='wagyu').first() or MenuItem.objects.first()
    wine  = MenuItem.objects.filter(name__icontains='wine').first() or MenuItem.objects.last()

    if admin:
        ord1, created = Order.objects.get_or_create(
            order_ref='ORD-882190',
            defaults={
                'user': admin,
                'customer_name': 'Admin Chef',
                'customer_email': 'admin@savoir.com',
                'customer_phone': '+1 (212) 555-0192',
                'order_type': 'pickup',
                'status': 'preparing',
                'subtotal': 185.00,
                'tax': 16.42,
                'total_price': 201.42,
                'notes': 'Medium rare steak, extra wine glass.'
            }
        )
        if created and steak and wine:
            OrderItem.objects.create(order=ord1, menu_item=steak, item_name=steak.name, unit_price=steak.price, quantity=2)
            OrderItem.objects.create(order=ord1, menu_item=wine, item_name=wine.name, unit_price=wine.price, quantity=1)

    if guest:
        ord2, created2 = Order.objects.get_or_create(
            order_ref='ORD-449102',
            defaults={
                'user': guest,
                'customer_name': 'Alexander Wright',
                'customer_email': 'guest@example.com',
                'customer_phone': '+1 (555) 349-2019',
                'order_type': 'delivery',
                'delivery_address': '742 Fifth Avenue, Penthouse B, NY',
                'status': 'completed',
                'subtotal': 120.00,
                'tax': 10.65,
                'total_price': 130.65,
                'notes': 'Please ring doorbell upon arrival.'
            }
        )
        if created2 and steak:
            OrderItem.objects.create(order=ord2, menu_item=steak, item_name=steak.name, unit_price=steak.price, quantity=1)

    print("Sample orders seeded successfully!")

if __name__ == '__main__':
    seed()
