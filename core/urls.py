from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView  # ✅ Add this
from . import views

urlpatterns = [
    path('signup/', views.signup_email_view, name='signup_email'),
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
    path('', views.home, name='home'),
    path('monument/<int:monument_id>/', views.monument_detail, name='monument_detail'),
    path('book/<int:id>/', views.book_ticket, name='book_ticket'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('create-checkout-session/<int:id>/', views.create_checkout_session, name='create_checkout_session'),
    path('chatbot-response/', views.chatbot_response, name='chatbot_response'), 
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
