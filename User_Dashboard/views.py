from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
import json

from .models import (MenuItem, MenuCategory, GalleryImage, TeamMember, Testimonial,
                    Reservation, UserProfile, Order, OrderItem)
from .forms import (ContactForm, ReservationForm, LoginForm, RegisterForm,
                    ForgotPasswordForm, ResetPasswordForm, UserInfoForm, ProfileForm)


# ═══════════════════════════════════════════
# PUBLIC PAGES
# ═══════════════════════════════════════════
def index(request):
    featured_items = MenuItem.objects.filter(is_featured=True, is_available=True).select_related('category')[:6]
    categories     = MenuCategory.objects.all()[:4]
    testimonials   = Testimonial.objects.filter(is_active=True)[:6]
    gallery_teaser = GalleryImage.objects.filter(is_active=True)[:6]
    return render(request, 'index.html', {
        'featured_items': featured_items,
        'categories':     categories,
        'testimonials':   testimonials,
        'gallery_teaser': gallery_teaser,
    })


def about(request):
    team = TeamMember.objects.filter(is_active=True)
    return render(request, 'about.html', {'team': team})


def gallery(request):
    category_filter = request.GET.get('category', '')
    images = GalleryImage.objects.filter(is_active=True)
    if category_filter:
        images = images.filter(category=category_filter)
    category_choices = GalleryImage.CATEGORY_CHOICES
    return render(request, 'gallery.html', {
        'images':           images,
        'category_choices': category_choices,
        'active_filter':    category_filter,
    })


def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you! Your message has been sent. We'll get back to you within 24 hours.")
            return redirect('contact')
    return render(request, 'contact.html', {'form': form})


def menu(request):
    categories = MenuCategory.objects.prefetch_related('items').all()
    all_items  = MenuItem.objects.filter(is_available=True).select_related('category')

    cat_slug = request.GET.get('category', '')
    dietary  = request.GET.get('dietary', '')
    search   = request.GET.get('q', '')

    if cat_slug:
        all_items = all_items.filter(category__slug=cat_slug)
    if dietary == 'veg':
        all_items = all_items.filter(is_vegetarian=True)
    elif dietary == 'vegan':
        all_items = all_items.filter(is_vegan=True)
    elif dietary == 'gf':
        all_items = all_items.filter(is_gluten_free=True)

    if search:
        all_items = all_items.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(ingredients__icontains=search)
        )

    grouped_menu = {}
    for cat in MenuCategory.objects.all():
        items_in_cat = [item for item in all_items if item.category_id == cat.id]
        if items_in_cat:
            grouped_menu[cat] = items_in_cat

    return render(request, 'menu.html', {
        'categories':      categories,
        'grouped_menu':    grouped_menu,
        'all_items':       all_items,
        'active_category': cat_slug,
        'active_dietary':  dietary,
        'search_query':    search,
    })


def dish_detail(request, pk):
    dish = get_object_or_404(MenuItem, pk=pk, is_available=True)
    similar_dishes = MenuItem.objects.filter(category=dish.category, is_available=True).exclude(pk=dish.pk)[:3]
    return render(request, 'dish-details.html', {
        'dish':           dish,
        'similar_dishes': similar_dishes,
    })


# ═══════════════════════════════════════════
# RESERVATIONS (LOGIN REQUIRED TO BOOK)
# ═══════════════════════════════════════════
def reservation(request):
    if not request.user.is_authenticated:
        messages.warning(request, "Please log in or create an account to book a table.")
        return redirect('/login/?next=/reservation/&tab=login')

    initial = {
        'name':  f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
        'email': request.user.email,
    }
    if hasattr(request.user, 'profile') and request.user.profile.phone:
        initial['phone'] = request.user.profile.phone

    form = ReservationForm(initial=initial)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            res = form.save(commit=False)
            res.user = request.user
            res.save()
            messages.success(request, f"Table reservation submitted! Reference: {res.booking_ref}")
            return redirect('reservation_success', ref=res.booking_ref)
        else:
            messages.error(request, "Please check the reservation form for errors below.")

    return render(request, 'reservation.html', {'form': form})


def reservation_success(request, ref):
    res = get_object_or_404(Reservation, booking_ref=ref)
    return render(request, 'reservation-success.html', {'reservation': res})


# ═══════════════════════════════════════════
# AUTHENTICATION
# ═══════════════════════════════════════════
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    active_tab = request.GET.get('tab', 'login')
    login_form = LoginForm()
    register_form = RegisterForm()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'login':
            active_tab = 'login'
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                username_or_email = login_form.cleaned_data['username']
                password = login_form.cleaned_data['password']

                user_obj = User.objects.filter(Q(username=username_or_email) | Q(email=username_or_email)).first()
                if user_obj:
                    user = authenticate(request, username=user_obj.username, password=password)
                    if user is not None:
                        login(request, user)
                        messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                        next_url = request.GET.get('next', 'dashboard')
                        return redirect(next_url)

                messages.error(request, "Invalid username/email or password.")

        elif action == 'register':
            active_tab = 'register'
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                user = User.objects.create_user(
                    username=register_form.cleaned_data['username'],
                    email=register_form.cleaned_data['email'],
                    password=register_form.cleaned_data['password'],
                    first_name=register_form.cleaned_data['first_name'],
                    last_name=register_form.cleaned_data['last_name']
                )
                login(request, user)
                messages.success(request, f"Welcome to Savoir, {user.first_name}! Your account has been created.")
                next_url = request.GET.get('next', 'dashboard')
                return redirect(next_url)
            else:
                messages.error(request, "Please correct the registration errors below.")

    return render(request, 'login.html', {
        'login_form':    login_form,
        'register_form': register_form,
        'active_tab':    active_tab,
    })


def register_view(request):
    return redirect('/login/?tab=register')


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')


def forgot_password_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = ForgotPasswordForm()
    success_sent = False
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user_exists = User.objects.filter(email=email).exists()
            success_sent = True
            if user_exists:
                messages.success(request, "Password reset link has been sent to your email.")

    return render(request, 'forgot-password.html', {'form': form, 'success_sent': success_sent})


def reset_password_view(request):
    form = ResetPasswordForm()
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            messages.success(request, "Your password has been successfully reset! You can now log in.")
            return redirect('login')

    return render(request, 'reset-password.html', {'form': form})


# ═══════════════════════════════════════════
# CUSTOMER DASHBOARD & ACCOUNT PAGES
# ═══════════════════════════════════════════

@login_required
def dashboard(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    recent_reservations = Reservation.objects.filter(user=request.user)[:3]
    recent_orders       = Order.objects.filter(user=request.user)[:3]

    total_reservations = Reservation.objects.filter(user=request.user).count()
    total_orders       = Order.objects.filter(user=request.user).count()
    upcoming_res       = Reservation.objects.filter(user=request.user, status__in=['pending', 'confirmed']).count()

    return render(request, 'dashboard.html', {
        'profile':             profile,
        'recent_reservations': recent_reservations,
        'recent_orders':       recent_orders,
        'total_reservations':  total_reservations,
        'total_orders':        total_orders,
        'upcoming_res':        upcoming_res,
    })


@login_required
def my_orders(request):
    status_filter = request.GET.get('status', 'all')
    orders = Order.objects.filter(user=request.user)

    if status_filter != 'all':
        orders = orders.filter(status=status_filter)

    return render(request, 'my-orders.html', {
        'orders':        orders,
        'status_filter': status_filter,
    })


@login_required
def order_details(request, ref):
    if request.user.is_staff:
        order = get_object_or_404(Order, order_ref=ref)
    else:
        order = get_object_or_404(Order, order_ref=ref, user=request.user)

    return render(request, 'order-details.html', {
        'order': order,
    })


@login_required
def my_reservations(request):
    status_filter = request.GET.get('status', 'all')
    reservations  = Reservation.objects.filter(user=request.user)

    if status_filter == 'upcoming':
        reservations = reservations.filter(status__in=['pending', 'confirmed'])
    elif status_filter != 'all':
        reservations = reservations.filter(status=status_filter)

    return render(request, 'my-reservations.html', {
        'reservations':  reservations,
        'status_filter': status_filter,
    })


@login_required
def reservation_details(request, ref):
    if request.user.is_staff:
        reservation_obj = get_object_or_404(Reservation, booking_ref=ref)
    else:
        reservation_obj = get_object_or_404(Reservation, booking_ref=ref, user=request.user)

    return render(request, 'reservation-details.html', {
        'reservation': reservation_obj,
    })


@login_required
def cancel_reservation(request, ref):
    reservation_obj = get_object_or_404(Reservation, booking_ref=ref, user=request.user)
    if request.method == 'POST' and reservation_obj.status in ['pending', 'confirmed']:
        reservation_obj.status = 'cancelled'
        reservation_obj.save()
        messages.success(request, f"Reservation {reservation_obj.booking_ref} has been cancelled.")
    return redirect('my_reservations')


@login_required
def profile_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    user_form = UserInfoForm(instance=request.user)
    profile_form = ProfileForm(instance=profile)

    if request.method == 'POST':
        user_form = UserInfoForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile details have been updated!")
            return redirect('profile')

    reservations = Reservation.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'profile.html', {
        'user_form':    user_form,
        'profile_form': profile_form,
        'profile':      profile,
        'reservations': reservations,
    })


# ═══════════════════════════════════════════
# 🛒 DEDICATED ORDERS CHECKOUT FLOW (5-PAGES)
# ═══════════════════════════════════════════

@login_required
def cart_view(request):
    """Step 1: Shopping Cart Page"""
    return render(request, 'orders/cart.html')


@login_required
def checkout_view(request):
    """Step 2: Delivery & Customer Info Details Page"""
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'orders/checkout.html', {
        'profile': profile,
    })


@login_required
def payment_view(request):
    """Step 3: Payment Selection & Tip Page"""
    return render(request, 'orders/payment.html')


@login_required
def process_payment(request):
    """Step 4: Process Payment & Save Order DB Record"""
    if request.method == 'POST':
        try:
            name       = request.POST.get('name') or f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            email      = request.POST.get('email') or request.user.email
            phone      = request.POST.get('phone') or ''
            order_type = request.POST.get('order_type', 'pickup')
            address    = request.POST.get('address', '')
            notes      = request.POST.get('notes', '')
            cart_json  = request.POST.get('cart_data', '[]')
            tip_amount = float(request.POST.get('tip', 0.0))

            cart_items = json.loads(cart_json)

            if not cart_items:
                messages.error(request, "Your cart was empty. Please add dishes to order.")
                return redirect('cart')

            subtotal = sum(float(item['price']) * int(item['qty']) for item in cart_items)
            tax = subtotal * 0.08875
            total = subtotal + tax + tip_amount

            order = Order.objects.create(
                user=request.user,
                customer_name=name,
                customer_email=email,
                customer_phone=phone,
                order_type=order_type,
                delivery_address=address,
                subtotal=subtotal,
                tax=tax,
                total_price=total,
                notes=notes,
                status='preparing',
            )

            for item in cart_items:
                menu_obj = MenuItem.objects.filter(name=item['name']).first()
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_obj,
                    item_name=item['name'],
                    unit_price=item['price'],
                    quantity=item['qty'],
                )

            messages.success(request, f"Order #{order.order_ref} confirmed & sent to kitchen!")
            return redirect('order_success', ref=order.order_ref)

        except Exception as e:
            messages.error(request, f"Error processing order: {e}")
            return redirect('checkout')

    return redirect('cart')


@login_required
def order_success_view(request, ref):
    """Step 4 Receipt: Order Confirmation & Success Page"""
    order = get_object_or_404(Order, order_ref=ref, user=request.user)
    return render(request, 'orders/order-success.html', {
        'order': order,
    })


@login_required
def track_order_view(request, ref):
    """Step 5: Live Order Progress Tracking Page"""
    order = get_object_or_404(Order, order_ref=ref, user=request.user)
    return render(request, 'orders/track-order.html', {
        'order': order,
    })


def place_order(request):
    """Legacy drawer shortcut POST view"""
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.warning(request, "Please log in or create an account to place your food pre-order.")
            return redirect('/login/?next=/orders/cart/&tab=login')
        return redirect('checkout')
    return redirect('cart')
