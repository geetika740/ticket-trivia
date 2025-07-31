from django.urls import path
from . import views

urlpatterns = [
    # Main Pages
    path('', views.monument_list_view, name='home'),  # ✅ Default route shows list of monuments
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    # Authentication
    path('signup/', views.signup_view, name='signup'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Booking
    path('monument/<int:monument_id>/', views.monument_detail, name='monument_detail'),
    path('book/<int:id>/', views.book_ticket, name='book_ticket'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('create-checkout-session/<int:id>/', views.create_checkout_session, name='create_checkout_session'),

    # Chatbot
    path('chatbot-response/', views.chatbot_response, name='chatbot_response'),
]
