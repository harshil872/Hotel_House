from django.urls import path
from . import views

urlpatterns = [
    path('',                             views.index,               name='index'),
    path('menu/',                        views.menu,                name='menu'),
    path('dish/<int:pk>/',               views.dish_detail,         name='dish_detail'),
    path('about/',                       views.about,               name='about'),
    path('gallery/',                     views.gallery,             name='gallery'),
    path('contact/',                     views.contact,             name='contact'),
    path('reservation/',                 views.reservation,         name='reservation'),
    path('reservation/success/<str:ref>/', views.reservation_success, name='reservation_success'),

    # ── Auth & Profile ────────────────────
    path('login/',           views.login_view,           name='login'),
    path('register/',        views.register_view,        name='register'),
    path('logout/',          views.logout_view,          name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/',  views.reset_password_view,  name='reset_password'),
    path('profile/',         views.profile_view,         name='profile'),

    # ── Customer Dashboard ────────────────
    path('dashboard/',                   views.dashboard,           name='dashboard'),
    path('my-orders/',                   views.my_orders,           name='my_orders'),
    path('order/<str:ref>/',             views.order_details,       name='order_details'),
    path('my-reservations/',             views.my_reservations,     name='my_reservations'),
    path('reservation-detail/<str:ref>/',views.reservation_details, name='reservation_details'),
    path('cancel-reservation/<str:ref>/',views.cancel_reservation,  name='cancel_reservation'),

    # ── Dedicated 5-Step Order Checkout Flow ──
    path('orders/cart/',                 views.cart_view,           name='cart'),
    path('orders/checkout/',             views.checkout_view,       name='checkout'),
    path('orders/payment/',              views.payment_view,        name='payment'),
    path('orders/process-payment/',      views.process_payment,     name='process_payment'),
    path('orders/success/<str:ref>/',    views.order_success_view,  name='order_success'),
    path('orders/track/<str:ref>/',      views.track_order_view,    name='track_order'),
    path('place-order/',                 views.place_order,         name='place_order'),
]
