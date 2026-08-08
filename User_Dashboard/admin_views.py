import csv
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.http import HttpResponse, JsonResponse
from django.utils.text import slugify
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from .models import (MenuItem, MenuCategory, Reservation, Order, OrderItem,
                    UserProfile, ContactMessage, Testimonial, GalleryImage,
                    Table, Offer, CulinaryEvent, RestaurantSetting)


# Helper decorator to redirect unauthenticated/non-staff users to custom /savoir_admin/ login page
def staff_required(view_func):
    return staff_member_required(view_func, login_url='savoir_admin')


# 0. Custom Staff Admin Login Portal View
def admin_login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user_obj = User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()
        if user_obj:
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None and user.is_staff:
                login(request, user)
                messages.success(request, f"Welcome back to Savoir Management Portal, {user.first_name or user.username}!")
                next_url = request.GET.get('next', '')
                if next_url:
                    return redirect(next_url)
                return redirect('admin_dashboard')
            elif user is not None and not user.is_staff:
                messages.error(request, "Access denied. Account lacks staff administrator permissions.")
            else:
                messages.error(request, "Invalid administrator credentials.")
        else:
            messages.error(request, "Invalid administrator credentials.")

    return render(request, 'admin_panel/admin_login.html')


# 1. Admin Master Dashboard Overview
@staff_required
def admin_dashboard(request):
    total_orders = Order.objects.count()
    total_revenue_val = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0.0
    total_revenue = round(float(total_revenue_val), 2)
    pending_reservations = Reservation.objects.filter(status='pending').count()
    total_dishes = MenuItem.objects.count()
    total_customers = User.objects.filter(is_staff=False).count()
    unread_messages = ContactMessage.objects.filter(is_resolved=False).count()
    
    recent_orders = Order.objects.all().order_by('-created_at')[:5]
    recent_reservations = Reservation.objects.all().order_by('-created_at')[:5]

    return render(request, 'admin_panel/dashboard.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_reservations': pending_reservations,
        'total_dishes': total_dishes,
        'total_customers': total_customers,
        'unread_messages': unread_messages,
        'recent_orders': recent_orders,
        'recent_reservations': recent_reservations,
    })


# 2. Reservations List Manager
@staff_required
def admin_reservations(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        ref = request.POST.get('booking_ref')
        if ref:
            res = get_object_or_404(Reservation, booking_ref=ref)
            if action == 'confirm':
                res.status = 'confirmed'
                res.save()
                messages.success(request, f"Reservation #{res.booking_ref} confirmed.")
            elif action == 'cancel':
                res.status = 'cancelled'
                res.save()
                messages.success(request, f"Reservation #{res.booking_ref} cancelled.")
            elif action == 'complete':
                res.status = 'completed'
                res.save()
                messages.success(request, f"Reservation #{res.booking_ref} marked as completed.")
            elif action == 'delete':
                res.delete()
                messages.success(request, "Reservation record deleted.")
            return redirect('admin_reservations')

    status_filter = request.GET.get('status')
    reservations = Reservation.objects.all()
    if status_filter:
        reservations = reservations.filter(status=status_filter)

    return render(request, 'admin_panel/reservations.html', {
        'reservations': reservations,
        'status_filter': status_filter,
    })


# 3. Single Reservation Detail Page
@staff_required
def admin_reservation_details(request, ref):
    res = get_object_or_404(Reservation, booking_ref=ref)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        new_seating = request.POST.get('seating_preference')
        notes = request.POST.get('special_requests')

        if new_status in dict(Reservation.STATUS_CHOICES):
            res.status = new_status
        if new_seating:
            res.seating_preference = new_seating
        if notes is not None:
            res.special_requests = notes

        res.save()
        messages.success(request, f"Reservation #{res.booking_ref} details updated successfully.")
        return redirect('admin_reservation_details', ref=res.booking_ref)

    return render(request, 'admin_panel/reservation-details.html', {'res': res})


# 4. Orders List Manager
@staff_required
def admin_orders(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        order_ref = request.POST.get('order_ref')
        if order_ref:
            order = get_object_or_404(Order, order_ref=order_ref)
            if action == 'preparing':
                order.status = 'preparing'
                order.save()
                messages.success(request, f"Order #{order.order_ref} sent to kitchen.")
            elif action == 'ready':
                order.status = 'ready'
                order.save()
                messages.success(request, f"Order #{order.order_ref} marked ready.")
            elif action == 'complete':
                order.status = 'completed'
                order.save()
                messages.success(request, f"Order #{order.order_ref} marked completed.")
            elif action == 'cancel':
                order.status = 'cancelled'
                order.save()
                messages.success(request, f"Order #{order.order_ref} cancelled.")
            elif action == 'delete':
                order.delete()
                messages.success(request, "Order record deleted.")
            return redirect('admin_orders')

    status_filter = request.GET.get('status')
    orders = Order.objects.all()
    if status_filter:
        orders = orders.filter(status=status_filter)

    return render(request, 'admin_panel/orders.html', {
        'orders': orders,
        'status_filter': status_filter,
    })


# 5. Single Order Detail Page
@staff_required
def admin_order_details(request, ref):
    order = get_object_or_404(Order, order_ref=ref)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            messages.success(request, f"Order #{order.order_ref} status updated to {order.get_status_display()}.")
            return redirect('admin_order_details', ref=order.order_ref)

    return render(request, 'admin_panel/order-details.html', {'order': order})


# 6. Live Kitchen Display System (KDS)
@staff_required
def admin_kitchen(request):
    if request.method == 'POST':
        order_ref = request.POST.get('order_ref')
        next_status = request.POST.get('next_status')
        if order_ref and next_status:
            order = get_object_or_404(Order, order_ref=order_ref)
            order.status = next_status
            order.save()
            messages.success(request, f"Order #{order.order_ref} updated to '{next_status}'.")
            return redirect('admin_kitchen')

    active_orders = Order.objects.filter(status__in=['pending', 'preparing', 'ready']).order_by('created_at')
    return render(request, 'admin_panel/kitchen.html', {'active_orders': active_orders})


@staff_required
def admin_kitchen_api(request):
    active_orders = Order.objects.filter(status__in=['pending', 'preparing', 'ready']).order_by('created_at').prefetch_related('items')
    orders_data = []
    for order in active_orders:
        items_data = [
            {
                'item_name': item.item_name,
                'quantity': item.quantity,
                'unit_price': float(item.unit_price),
            }
            for item in order.items.all()
        ]
        orders_data.append({
            'order_ref': order.order_ref,
            'customer_name': order.customer_name,
            'order_type': order.get_order_type_display(),
            'status': order.status,
            'status_display': order.get_status_display(),
            'notes': order.notes,
            'created_at': order.created_at.strftime('%I:%M %p'),
            'total_price': float(order.total_price),
            'items': items_data,
        })
    return JsonResponse({'orders': orders_data, 'count': len(orders_data)})


# 7. Menu Dishes Catalog Manager
@staff_required
def admin_menu(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        dish_id = request.POST.get('dish_id')
        if dish_id:
            dish = get_object_or_404(MenuItem, pk=dish_id)
            if action == 'toggle_available':
                dish.is_available = not dish.is_available
                dish.save()
                messages.success(request, f"Availability toggled for '{dish.name}'.")
            elif action == 'delete':
                dish.delete()
                messages.success(request, "Dish deleted from menu.")
            return redirect('admin_menu')

    dishes = MenuItem.objects.all().select_related('category')
    return render(request, 'admin_panel/menu.html', {'dishes': dishes})


# 8. Add Dish Form
@staff_required
def admin_add_dish(request):
    categories = MenuCategory.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category')
        price = request.POST.get('price')
        description = request.POST.get('description', '')
        spice_level = request.POST.get('spice_level', 'none')
        ingredients = request.POST.get('ingredients', '')
        chef_notes = request.POST.get('chef_notes', '')

        is_veg = 'is_vegetarian' in request.POST or 'is_veg' in request.POST
        is_gf = 'is_gluten_free' in request.POST or 'is_gf' in request.POST
        is_featured = 'is_featured' in request.POST
        is_available = 'is_available' in request.POST

        category = get_object_or_404(MenuCategory, id=category_id)
        dish = MenuItem.objects.create(
            category=category,
            name=name,
            price=price,
            description=description,
            spice_level=spice_level,
            ingredients=ingredients,
            chef_notes=chef_notes,
            is_vegetarian=is_veg,
            is_gluten_free=is_gf,
            is_featured=is_featured,
            is_available=is_available,
        )

        if 'image' in request.FILES:
            dish.image = request.FILES['image']
            dish.save()

        messages.success(request, f"Dish '{name}' added successfully.")
        return redirect('admin_menu')

    return render(request, 'admin_panel/add-dish.html', {'categories': categories})


# 9. Edit Dish Form
@staff_required
def admin_edit_dish(request, pk):
    dish = get_object_or_404(MenuItem, pk=pk)
    categories = MenuCategory.objects.all()
    if request.method == 'POST':
        dish.name = request.POST.get('name')
        category_id = request.POST.get('category')
        dish.category = get_object_or_404(MenuCategory, id=category_id)
        dish.price = request.POST.get('price')
        dish.description = request.POST.get('description', '')
        dish.spice_level = request.POST.get('spice_level', 'none')
        dish.ingredients = request.POST.get('ingredients', '')
        dish.chef_notes = request.POST.get('chef_notes', '')

        dish.is_vegetarian = 'is_vegetarian' in request.POST or 'is_veg' in request.POST
        dish.is_gluten_free = 'is_gluten_free' in request.POST or 'is_gf' in request.POST
        dish.is_featured = 'is_featured' in request.POST
        dish.is_available = 'is_available' in request.POST

        if 'image' in request.FILES:
            dish.image = request.FILES['image']

        dish.save()
        messages.success(request, f"Dish '{dish.name}' updated successfully.")
        return redirect('admin_menu')

    return render(request, 'admin_panel/edit-dish.html', {'dish': dish, 'categories': categories})


# 10. Menu Categories Manager
@staff_required
def admin_categories(request):
    categories = MenuCategory.objects.all()
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            icon = request.POST.get('icon', '')
            if name:
                slug = slugify(name)
                MenuCategory.objects.create(name=name, slug=slug, description=description, icon=icon)
                messages.success(request, f"Category '{name}' created successfully.")
        elif action == 'delete':
            cat_id = request.POST.get('category_id')
            if cat_id:
                cat = get_object_or_404(MenuCategory, pk=cat_id)
                cat.delete()
                messages.success(request, "Category deleted.")
        return redirect('admin_categories')

    return render(request, 'admin_panel/categories.html', {'categories': categories})


# 11. Floor Plan & Tables Manager
@staff_required
def admin_tables(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            table_num = request.POST.get('table_number')
            capacity = request.POST.get('capacity', 4)
            location = request.POST.get('location', 'main')
            if table_num:
                Table.objects.create(table_number=table_num, capacity=capacity, location=location)
                messages.success(request, f"Table #{table_num} created.")
        elif action == 'toggle_occupied':
            table_id = request.POST.get('table_id')
            table = get_object_or_404(Table, pk=table_id)
            table.is_occupied = not table.is_occupied
            table.save()
            messages.success(request, f"Table #{table.table_number} occupancy status updated.")
        elif action == 'delete':
            table_id = request.POST.get('table_id')
            table = get_object_or_404(Table, pk=table_id)
            table.delete()
            messages.success(request, "Table removed from floor plan.")
        return redirect('admin_tables')

    tables = Table.objects.all()
    return render(request, 'admin_panel/tables.html', {'tables': tables})


# 12. Customer CRM Database Manager
@staff_required
def admin_customers(request):
    customers = User.objects.filter(is_staff=False).select_related('profile').prefetch_related('reservations', 'orders')
    return render(request, 'admin_panel/customers.html', {'customers': customers})


# 13. Guest Reviews & Testimonials Manager
@staff_required
def admin_reviews(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            name = request.POST.get('name')
            rating = request.POST.get('rating', 5)
            review = request.POST.get('review')
            source = request.POST.get('source', 'Website')
            if name and review:
                Testimonial.objects.create(name=name, rating=rating, review=review, source=source)
                messages.success(request, "New guest testimonial added.")
        elif action == 'toggle_active':
            rev_id = request.POST.get('review_id')
            rev = get_object_or_404(Testimonial, pk=rev_id)
            rev.is_active = not rev.is_active
            rev.save()
            messages.success(request, "Review status updated.")
        elif action == 'delete':
            rev_id = request.POST.get('review_id')
            rev = get_object_or_404(Testimonial, pk=rev_id)
            rev.delete()
            messages.success(request, "Review deleted.")
        return redirect('admin_reviews')

    reviews = Testimonial.objects.all()
    return render(request, 'admin_panel/reviews.html', {'reviews': reviews})


# 14. Offers & Promo Coupons Manager
@staff_required
def admin_offers(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            code = request.POST.get('code')
            title = request.POST.get('title')
            discount = request.POST.get('discount_percent', 10)
            if code and title:
                Offer.objects.create(code=code.upper(), title=title, discount_percent=discount)
                messages.success(request, f"Promo code '{code.upper()}' created.")
        elif action == 'toggle_active':
            offer_id = request.POST.get('offer_id')
            offer = get_object_or_404(Offer, pk=offer_id)
            offer.is_active = not offer.is_active
            offer.save()
            messages.success(request, f"Coupon '{offer.code}' status updated.")
        elif action == 'delete':
            offer_id = request.POST.get('offer_id')
            offer = get_object_or_404(Offer, pk=offer_id)
            offer.delete()
            messages.success(request, "Coupon offer deleted.")
        return redirect('admin_offers')

    offers = Offer.objects.all()
    return render(request, 'admin_panel/offers.html', {'offers': offers})


# 15. Culinary Events Manager
@staff_required
def admin_events(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            title = request.POST.get('title')
            date = request.POST.get('date')
            time = request.POST.get('time', '7:00 PM')
            price = request.POST.get('price', 150)
            capacity = request.POST.get('capacity', 30)
            desc = request.POST.get('description', '')
            if title and date:
                CulinaryEvent.objects.create(title=title, date=date, time=time, price=price, capacity=capacity, description=desc)
                messages.success(request, f"Culinary event '{title}' scheduled.")
        elif action == 'toggle_active':
            event_id = request.POST.get('event_id')
            event = get_object_or_404(CulinaryEvent, pk=event_id)
            event.is_active = not event.is_active
            event.save()
            messages.success(request, f"Event '{event.title}' status updated.")
        elif action == 'delete':
            event_id = request.POST.get('event_id')
            event = get_object_or_404(CulinaryEvent, pk=event_id)
            event.delete()
            messages.success(request, "Culinary event deleted.")
        return redirect('admin_events')

    events = CulinaryEvent.objects.all()
    return render(request, 'admin_panel/events.html', {'events': events})


# 16. Photo Gallery Assets Manager
@staff_required
def admin_gallery(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'upload':
            caption = request.POST.get('caption', '')
            category = request.POST.get('category', 'food')
            if 'image' in request.FILES:
                GalleryImage.objects.create(image=request.FILES['image'], caption=caption, category=category)
                messages.success(request, "Photo uploaded to gallery.")
        elif action == 'toggle_active':
            img_id = request.POST.get('image_id')
            img = get_object_or_404(GalleryImage, pk=img_id)
            img.is_active = not img.is_active
            img.save()
            messages.success(request, "Gallery image visibility updated.")
        elif action == 'delete':
            img_id = request.POST.get('image_id')
            img = get_object_or_404(GalleryImage, pk=img_id)
            img.delete()
            messages.success(request, "Gallery photo removed.")
        return redirect('admin_gallery')

    images = GalleryImage.objects.all()
    return render(request, 'admin_panel/gallery.html', {'images': images})


# 17. Contact Inquiry Messages Inbox
@staff_required
def admin_messages(request):
    if request.method == 'POST':
        action = request.POST.get('action')
        msg_id = request.POST.get('message_id')
        if msg_id:
            msg_obj = get_object_or_404(ContactMessage, pk=msg_id)
            if action == 'toggle_resolved':
                msg_obj.is_resolved = not msg_obj.is_resolved
                msg_obj.save()
                messages.success(request, f"Message status updated to {'Resolved' if msg_obj.is_resolved else 'Unresolved'}.")
            elif action == 'delete':
                msg_obj.delete()
                messages.success(request, "Message deleted.")
            return redirect('admin_messages')

    msgs = ContactMessage.objects.all()
    return render(request, 'admin_panel/messages.html', {'msgs': msgs})


# 18. Analytics & Financial Reports
@staff_required
def admin_reports(request):
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="savoir_financial_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Order Ref', 'Customer Name', 'Customer Email', 'Order Type', 'Status', 'Subtotal ($)', 'Tax ($)', 'Total Price ($)', 'Created At'])
        
        orders = Order.objects.all().order_by('-created_at')
        for order in orders:
            writer.writerow([
                order.order_ref,
                order.customer_name,
                order.customer_email,
                order.order_type,
                order.status,
                order.subtotal,
                order.tax,
                order.total_price,
                order.created_at.strftime('%Y-%m-%d %H:%M') if hasattr(order, 'created_at') and order.created_at else ''
            ])
        return response

    total_orders = Order.objects.count()
    total_revenue_val = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0.0
    total_revenue = round(float(total_revenue_val), 2)
    avg_order_value = round(total_revenue / total_orders, 2) if total_orders > 0 else 0.0
    
    total_reservations = Reservation.objects.count()
    total_customers = User.objects.filter(is_staff=False).count()
    
    pickup_count = Order.objects.filter(order_type='pickup').count()
    delivery_count = Order.objects.filter(order_type='delivery').count()
    dinein_count = Order.objects.filter(order_type='dinein').count()
    
    top_items = OrderItem.objects.values('item_name').annotate(
        total_qty=Sum('quantity'),
        total_sales=Sum('unit_price')
    ).order_by('-total_qty')[:5]

    recent_orders = Order.objects.all().order_by('-created_at')[:10]

    return render(request, 'admin_panel/reports.html', {
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'avg_order_value': avg_order_value,
        'total_reservations': total_reservations,
        'total_customers': total_customers,
        'pickup_count': pickup_count,
        'delivery_count': delivery_count,
        'dinein_count': dinein_count,
        'top_items': top_items,
        'recent_orders': recent_orders,
    })


# 19. Restaurant System General Settings
@staff_required
def admin_settings(request):
    setting, _ = RestaurantSetting.objects.get_or_create(id=1)
    if request.method == 'POST':
        setting.brand_name = request.POST.get('brand_name', setting.brand_name)
        setting.phone = request.POST.get('phone', setting.phone)
        setting.email = request.POST.get('email', setting.email)
        setting.tax_rate = request.POST.get('tax_rate', setting.tax_rate)
        setting.address = request.POST.get('address', setting.address)
        setting.opening_hours = request.POST.get('opening_hours', setting.opening_hours)
        setting.save()
        messages.success(request, "Restaurant operating configurations saved successfully!")
        return redirect('admin_settings')

    return render(request, 'admin_panel/settings.html', {'setting': setting})
