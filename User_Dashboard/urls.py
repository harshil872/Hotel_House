from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    # ── Public Guest Routes ───────────────
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

    # ── 👑 CUSTOM ADMIN PANEL (STAFF LOGIN PORTAL + 19 MANAGEMENT PAGES) ──
    path('savoir_admin/',                      admin_views.admin_login_view,          name='savoir_admin'),
    path('admin-panel/',                       admin_views.admin_login_view),
    path('admin-panel/dashboard/',             admin_views.admin_dashboard,           name='admin_dashboard'),
    path('admin-panel/reservations/',          admin_views.admin_reservations,        name='admin_reservations'),
    path('admin-panel/reservations/<str:ref>/',admin_views.admin_reservation_details,name='admin_reservation_details'),
    path('admin-panel/orders/',                admin_views.admin_orders,              name='admin_orders'),
    path('admin-panel/orders/<str:ref>/',      admin_views.admin_order_details,        name='admin_order_details'),
    path('admin-panel/kitchen/',               admin_views.admin_kitchen,             name='admin_kitchen'),
    path('admin-panel/api/kitchen-orders/',    admin_views.admin_kitchen_api,         name='admin_kitchen_api'),
    path('admin-panel/menu/',                  admin_views.admin_menu,                name='admin_menu'),
    path('admin-panel/add-dish/',              admin_views.admin_add_dish,            name='admin_add_dish'),
    path('admin-panel/edit-dish/<int:pk>/',    admin_views.admin_edit_dish,           name='admin_edit_dish'),
    path('admin-panel/categories/',            admin_views.admin_categories,          name='admin_categories'),
    path('admin-panel/tables/',                admin_views.admin_tables,              name='admin_tables'),
    path('admin-panel/customers/',             admin_views.admin_customers,           name='admin_customers'),
    path('admin-panel/reviews/',               admin_views.admin_reviews,             name='admin_reviews'),
    path('admin-panel/offers/',                admin_views.admin_offers,              name='admin_offers'),
    path('admin-panel/events/',                admin_views.admin_events,              name='admin_events'),
    path('admin-panel/gallery/',               admin_views.admin_gallery,             name='admin_gallery'),
    path('admin-panel/messages/',              admin_views.admin_messages,            name='admin_messages'),
    path('admin-panel/reports/',               admin_views.admin_reports,             name='admin_reports'),
    path('admin-panel/sessions/',              admin_views.admin_sessions,            name='admin_sessions'),
    path('admin-panel/sessions/<str:session_key>/', admin_views.admin_session_detail,   name='admin_session_detail'),
    path('admin-panel/settings/',              admin_views.admin_settings,            name='admin_settings'),
]

