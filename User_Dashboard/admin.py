from django.contrib import admin
from .models import (MenuCategory, MenuItem, GalleryImage, TeamMember,
                    Testimonial, ContactMessage, Reservation, UserProfile, Order, OrderItem,
                    Table, Offer, CulinaryEvent, RestaurantSetting)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['item_name', 'unit_price', 'quantity', 'get_total']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display  = ['order_ref', 'user', 'customer_name', 'order_type', 'total_price', 'status', 'created_at']
    list_filter   = ['status', 'order_type', 'created_at']
    list_editable = ['status']
    search_fields = ['order_ref', 'customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['order_ref', 'created_at']
    inlines       = [OrderItemInline]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'dietary_preferences', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone']


@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display  = ['name', 'slug', 'order']
    prepopulated_fields = {'slug': ('name',)}
    ordering      = ['order']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display  = ['name', 'category', 'price', 'spice_level', 'is_featured', 'is_available']
    list_filter   = ['category', 'is_featured', 'is_available', 'is_vegetarian', 'spice_level']
    list_editable = ['is_featured', 'is_available']
    search_fields = ['name', 'description', 'ingredients']
    ordering      = ['category', 'order']


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display  = ['caption', 'category', 'order', 'is_active']
    list_filter   = ['category', 'is_active']
    list_editable = ['order', 'is_active']
    ordering      = ['order']


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display  = ['name', 'role', 'specialty', 'order', 'is_active']
    list_editable = ['order', 'is_active']
    ordering      = ['order']


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display  = ['name', 'rating', 'source', 'is_active', 'date_posted']
    list_filter   = ['rating', 'is_active', 'source']
    list_editable = ['is_active']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display  = ['name', 'email', 'subject', 'is_resolved', 'created_at']
    list_filter   = ['subject', 'is_resolved']
    list_editable = ['is_resolved']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    search_fields = ['name', 'email', 'message']


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display  = ['booking_ref', 'user', 'name', 'date', 'time', 'guests', 'seating_preference', 'status', 'created_at']
    list_filter   = ['status', 'date', 'time', 'occasion', 'seating_preference']
    list_editable = ['status']
    search_fields = ['booking_ref', 'name', 'email', 'phone']
    readonly_fields = ['booking_ref', 'created_at']
    ordering      = ['-created_at']


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display  = ['table_number', 'capacity', 'location', 'is_occupied', 'is_active']
    list_editable = ['is_occupied', 'is_active']
    list_filter   = ['location', 'is_occupied', 'is_active']


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display  = ['code', 'title', 'discount_percent', 'valid_until', 'is_active']
    list_editable = ['is_active']


@admin.register(CulinaryEvent)
class CulinaryEventAdmin(admin.ModelAdmin):
    list_display  = ['title', 'date', 'time', 'price', 'capacity', 'is_active']
    list_editable = ['is_active']


@admin.register(RestaurantSetting)
class RestaurantSettingAdmin(admin.ModelAdmin):
    list_display  = ['brand_name', 'phone', 'email', 'tax_rate']