from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
import json

from .models import (
    MenuCategory, MenuItem, GalleryImage, TeamMember, Testimonial,
    ContactMessage, Reservation, Order, OrderItem, UserProfile, Table, Offer, CulinaryEvent, RestaurantSetting
)


class ModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testcustomer',
            email='customer@example.com',
            password='password123',
            first_name='John',
            last_name='Doe'
        )
        self.category = MenuCategory.objects.create(
            name='Starters',
            slug='starters',
            description='Delicious starters',
            order=1
        )
        self.menu_item = MenuItem.objects.create(
            category=self.category,
            name='Truffle Soup',
            description='Warm luxury truffle soup',
            price=24.50,
            ingredients='Black Truffle, Heavy Cream, Garlic',
            is_available=True,
            is_featured=True
        )

    def test_menu_category_str(self):
        self.assertEqual(str(self.category), 'Starters')

    def test_menu_item_str_and_ingredients(self):
        self.assertIn('Truffle Soup', str(self.menu_item))
        self.assertEqual(self.menu_item.get_ingredients_list(), ['Black Truffle', 'Heavy Cream', 'Garlic'])

    def test_user_profile_creation(self):
        profile, created = UserProfile.objects.get_or_create(user=self.user)
        self.assertIn('Profile — testcustomer', str(profile))

    def test_reservation_model(self):
        res = Reservation.objects.create(
            user=self.user,
            name='John Doe',
            email='customer@example.com',
            phone='1234567890',
            guests=2,
            date='2026-10-15',
            time='19:00',
            status='pending'
        )
        self.assertTrue(res.booking_ref.startswith('RES-'))
        self.assertIn('John Doe', str(res))

    def test_order_and_order_item_totals(self):
        order = Order.objects.create(
            user=self.user,
            customer_name='John Doe',
            customer_email='customer@example.com',
            customer_phone='1234567890',
            order_type='pickup',
            subtotal=24.50,
            tax=2.17,
            total_price=26.67
        )
        item = OrderItem.objects.create(
            order=order,
            menu_item=self.menu_item,
            item_name=self.menu_item.name,
            unit_price=self.menu_item.price,
            quantity=2
        )
        self.assertTrue(order.order_ref.startswith('ORD-'))
        self.assertEqual(item.get_total(), 49.00)


class PublicViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_page(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_menu_page(self):
        response = self.client.get(reverse('menu'))
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_gallery_page(self):
        response = self.client.get(reverse('gallery'))
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)

    def test_contact_form_submission(self):
        post_data = {
            'name': 'Alice Smith',
            'email': 'alice@example.com',
            'phone': '555-123-4567',
            'subject': 'general',
            'message': 'Hello, I love your restaurant!'
        }
        response = self.client.post(reverse('contact'), post_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(ContactMessage.objects.filter(email='alice@example.com').exists())


class CustomerAuthAndReservationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='Password123!',
            first_name='John',
            last_name='Doe'
        )

    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'action': 'login',
            'username': 'johndoe',
            'password': 'Password123!'
        })
        self.assertEqual(response.status_code, 302)

    def test_reservation_unauthenticated_redirect(self):
        response = self.client.get(reverse('reservation'))
        self.assertEqual(response.status_code, 302)

    def test_reservation_authenticated_booking(self):
        self.client.login(username='johndoe', password='Password123!')
        res_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '1234567890',
            'guests': 4,
            'date': '2026-11-20',
            'time': '18:30',
            'occasion': 'birthday',
            'seating_preference': 'main',
            'special_requests': 'Quiet table please'
        }
        response = self.client.post(reverse('reservation'), res_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Reservation.objects.filter(user=self.user).exists())


class AdminPanelSecurityAndKDSTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.customer = User.objects.create_user(
            username='regularuser',
            email='regular@example.com',
            password='Password123!'
        )
        self.staff_user = User.objects.create_user(
            username='adminstaff',
            email='admin@example.com',
            password='StaffPassword123!',
            is_staff=True
        )

    def test_admin_dashboard_access_denied_for_regular_user(self):
        self.client.login(username='regularuser', password='Password123!')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('savoir_admin', response.url)

    def test_admin_dashboard_access_granted_for_staff(self):
        self.client.login(username='adminstaff', password='StaffPassword123!')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_admin_kitchen_api(self):
        self.client.login(username='adminstaff', password='StaffPassword123!')
        Order.objects.create(
            customer_name='Jane Staff',
            customer_email='jane@example.com',
            customer_phone='9990001111',
            order_type='pickup',
            status='pending',
            total_price=50.00
        )
        response = self.client.get(reverse('admin_kitchen_api'))
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('orders', data)
        self.assertEqual(data['count'], 1)


class AdminSessionManagementTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username='sessionadmin',
            email='sessadmin@example.com',
            password='StaffPassword123!',
            is_staff=True
        )

    def test_admin_sessions_view_requires_staff(self):
        response = self.client.get(reverse('admin_sessions'))
        self.assertEqual(response.status_code, 302)

    def test_admin_sessions_view_staff_access(self):
        self.client.login(username='sessionadmin', password='StaffPassword123!')
        response = self.client.get(reverse('admin_sessions'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Active Sessions Register")

    def test_admin_session_detail_view(self):
        self.client.login(username='sessionadmin', password='StaffPassword123!')
        session_key = self.client.session.session_key
        response = self.client.get(reverse('admin_session_detail', args=[session_key]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Session Inspector")

    def test_admin_session_terminate_action(self):
        self.client.login(username='sessionadmin', password='StaffPassword123!')
        session_key = self.client.session.session_key
        response = self.client.post(reverse('admin_sessions'), {
            'action': 'terminate',
            'session_key': session_key
        })
        self.assertEqual(response.status_code, 302)

