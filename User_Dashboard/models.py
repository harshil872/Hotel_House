from django.db import models
from django.contrib.auth.models import User
import uuid


# ─────────────────────────────────────────
# USER PROFILE
# ─────────────────────────────────────────
class UserProfile(models.Model):
    user                 = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone                = models.CharField(max_length=20, blank=True)
    address              = models.TextField(blank=True)
    profile_photo        = models.ImageField(upload_to='profiles/', blank=True)
    dietary_preferences  = models.CharField(max_length=200, blank=True, help_text="e.g. Vegetarian, Gluten-Free, Nut Allergy")
    favorite_table_notes = models.TextField(blank=True)
    created_at           = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile — {self.user.username}"


# ─────────────────────────────────────────
# MENU CATEGORY
# ─────────────────────────────────────────
class MenuCategory(models.Model):
    name        = models.CharField(max_length=100)
    slug        = models.SlugField(unique=True)
    description = models.CharField(max_length=300, blank=True)
    icon        = models.CharField(max_length=50, blank=True, help_text="Font Awesome class e.g. fa-utensils")
    order       = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Menu Categories'


# ─────────────────────────────────────────
# MENU ITEM
# ─────────────────────────────────────────
class MenuItem(models.Model):
    SPICE_CHOICES = [
        ('none',   'Not Spicy'),
        ('mild',   'Mild'),
        ('medium', 'Medium'),
        ('hot',    'Hot'),
        ('extra',  'Extra Hot'),
    ]

    category      = models.ForeignKey(MenuCategory, on_delete=models.CASCADE, related_name='items')
    name          = models.CharField(max_length=200)
    description   = models.TextField()
    price         = models.DecimalField(max_digits=8, decimal_places=2)
    image         = models.ImageField(upload_to='menu/', blank=True)
    spice_level   = models.CharField(max_length=10, choices=SPICE_CHOICES, default='none')
    is_vegetarian = models.BooleanField(default=False)
    is_vegan      = models.BooleanField(default=False)
    is_gluten_free= models.BooleanField(default=False)
    is_featured   = models.BooleanField(default=False)
    is_available  = models.BooleanField(default=True)
    ingredients   = models.TextField(blank=True, help_text="Comma-separated ingredients e.g. Wagyu Beef, Black Truffle, Rosemary")
    prep_time     = models.PositiveIntegerField(default=20, help_text="Prep time in minutes")
    calories      = models.PositiveIntegerField(null=True, blank=True, help_text="Approximate calories per serving")
    chef_notes    = models.TextField(blank=True, help_text="Chef's pairing or preparation notes")
    order         = models.PositiveIntegerField(default=0)
    created_at    = models.DateTimeField(auto_now_add=True)

    def get_ingredients_list(self):
        if self.ingredients:
            return [i.strip() for i in self.ingredients.split(',') if i.strip()]
        return []

    def __str__(self):
        return f"{self.name} — ${self.price}"

    class Meta:
        ordering = ['order', 'name']


# ─────────────────────────────────────────
# GALLERY IMAGE
# ─────────────────────────────────────────
class GalleryImage(models.Model):
    CATEGORY_CHOICES = [
        ('food',      'Food & Dishes'),
        ('ambiance',  'Ambiance'),
        ('events',    'Events'),
        ('chefs',     'Our Chefs'),
        ('exterior',  'Exterior'),
    ]

    image    = models.ImageField(upload_to='gallery/')
    caption  = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='food')
    order    = models.PositiveIntegerField(default=0)
    is_active= models.BooleanField(default=True)

    def __str__(self):
        return f"{self.get_category_display()} — {self.caption or 'Image'}"

    class Meta:
        ordering = ['order']
        verbose_name = 'Gallery Image'


# ─────────────────────────────────────────
# TEAM MEMBER
# ─────────────────────────────────────────
class TeamMember(models.Model):
    name        = models.CharField(max_length=200)
    role        = models.CharField(max_length=100)
    bio         = models.TextField()
    photo       = models.ImageField(upload_to='team/', blank=True)
    specialty   = models.CharField(max_length=200, blank=True)
    instagram   = models.URLField(blank=True)
    order       = models.PositiveIntegerField(default=0)
    is_active   = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} — {self.role}"

    class Meta:
        ordering = ['order']


# ─────────────────────────────────────────
# TESTIMONIAL
# ─────────────────────────────────────────
class Testimonial(models.Model):
    name       = models.CharField(max_length=200)
    avatar     = models.ImageField(upload_to='testimonials/', blank=True)
    rating     = models.PositiveIntegerField(default=5)   # 1–5
    review     = models.TextField()
    source     = models.CharField(max_length=100, blank=True, help_text="e.g. Google, TripAdvisor, Yelp")
    date_posted= models.DateField(auto_now_add=True)
    is_active  = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.rating}★)"

    class Meta:
        ordering = ['-date_posted']


# ─────────────────────────────────────────
# CONTACT MESSAGE
# ─────────────────────────────────────────
class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('reservation',  'Table Reservation'),
        ('feedback',     'Feedback'),
        ('catering',     'Catering & Events'),
        ('general',      'General Inquiry'),
        ('partnership',  'Partnership'),
        ('press',        'Press & Media'),
    ]

    name        = models.CharField(max_length=200)
    email       = models.EmailField()
    phone       = models.CharField(max_length=20, blank=True)
    subject     = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='general')
    message     = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} — {self.get_subject_display()}"

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'


# ─────────────────────────────────────────
# TABLE RESERVATION
# ─────────────────────────────────────────
def generate_res_ref():
    return 'RES-' + uuid.uuid4().hex[:6].upper()


class Reservation(models.Model):
    TIME_CHOICES = [
        ('12:00', '12:00 PM (Lunch)'),
        ('12:30', '12:30 PM (Lunch)'),
        ('13:00', '1:00 PM (Lunch)'),
        ('13:30', '1:30 PM (Lunch)'),
        ('14:00', '2:00 PM (Lunch)'),
        ('18:00', '6:00 PM (Dinner)'),
        ('18:30', '6:30 PM (Dinner)'),
        ('19:00', '7:00 PM (Dinner)'),
        ('19:30', '7:30 PM (Dinner)'),
        ('20:00', '8:00 PM (Dinner)'),
        ('20:30', '8:30 PM (Dinner)'),
        ('21:00', '9:00 PM (Dinner)'),
    ]

    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    OCCASION_CHOICES = [
        ('casual',      'Casual Dining'),
        ('birthday',    'Birthday'),
        ('anniversary', 'Anniversary'),
        ('date',        'Date Night'),
        ('business',    'Business Meal'),
        ('celebration', 'Special Celebration'),
    ]

    SEATING_CHOICES = [
        ('main',     'Main Dining Room'),
        ('window',   'Window Table'),
        ('booth',    'Cozy Booth'),
        ('terrace',  'Outdoor Terrace'),
        ('chef',     'Chef\'s Table / Counter'),
        ('private',  'Private Dining Room'),
    ]

    user               = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    booking_ref        = models.CharField(max_length=20, unique=True, default=generate_res_ref)
    name               = models.CharField(max_length=200)
    email              = models.EmailField()
    phone              = models.CharField(max_length=20)
    guests             = models.PositiveIntegerField(default=2)
    date               = models.DateField()
    time               = models.CharField(max_length=10, choices=TIME_CHOICES)
    occasion           = models.CharField(max_length=50, choices=OCCASION_CHOICES, default='casual', blank=True)
    seating_preference = models.CharField(max_length=50, choices=SEATING_CHOICES, default='main', blank=True)
    special_requests   = models.TextField(blank=True)
    status             = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at         = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booking_ref} — {self.name} ({self.date} at {self.time})"

    class Meta:
        ordering = ['-created_at']


# ─────────────────────────────────────────
# FOOD PRE-ORDER / ORDER
# ─────────────────────────────────────────
def generate_order_ref():
    return 'ORD-' + uuid.uuid4().hex[:6].upper()


class Order(models.Model):
    TYPE_CHOICES = [
        ('pickup',   'Store Pickup'),
        ('delivery', 'Home Delivery'),
        ('dine_in',  'Pre-order for Table'),
    ]

    STATUS_CHOICES = [
        ('pending',   'Pending Confirmation'),
        ('preparing', 'Kitchen Preparing'),
        ('ready',     'Ready / Out for Delivery'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user             = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    order_ref        = models.CharField(max_length=20, unique=True, default=generate_order_ref)
    customer_name    = models.CharField(max_length=200)
    customer_email   = models.EmailField()
    customer_phone   = models.CharField(max_length=20)
    order_type       = models.CharField(max_length=20, choices=TYPE_CHOICES, default='pickup')
    delivery_address = models.TextField(blank=True)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    subtotal         = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax              = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_price      = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    notes            = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_ref} — {self.customer_name} (${self.total_price})"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order      = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item  = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True, blank=True)
    item_name  = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity   = models.PositiveIntegerField(default=1)

    def get_total(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.item_name} @ ${self.unit_price}"