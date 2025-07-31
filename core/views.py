from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Monument, Booking
from .forms import EmailForm, OTPForm
from django.contrib.auth.models import User
import random
from django.core.mail import send_mail
from django.conf import settings
import stripe
import json

# OTP store
otp_store = {}

# ------------------------------✅ Signup step 1: enter email----------------------------------
def signup_email_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})

        otp = str(random.randint(100000, 999999))
        otp_store[email] = {'otp': otp, 'username': username, 'password': password}

        send_mail(
            'Your OTP Code',
            f'Your OTP code is: {otp}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        return render(request, 'verify_otp.html', {'email': email})
    return render(request, 'signup.html')

# ------------------------------✅ OTP verification-----------------------------------------
def verify_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        entered_otp = request.POST.get('otp')

        if email in otp_store and otp_store[email]['otp'] == entered_otp:
            username = otp_store[email]['username']
            password = otp_store[email]['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            del otp_store[email]
            return redirect('home')
        else:
            return render(request, 'verify_otp.html', {'email': email, 'error': 'Invalid OTP'})
    return redirect('signup_email')

# ------------------------------✅ Login view------------------------------------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

# --------------------------------✅ Logout--------------------------------------------------
def logout_view(request):
    logout(request)
    return redirect('login')

# ---------------------------------✅ Homepage: monument/park/museum list---------------------------
def monument_list_view(request):
    monuments = Monument.objects.all()
    return render(request, 'home.html', {'monuments': monuments})

# ---------------------------------✅ Monument details------------------------------------------------
def monument_detail(request, monument_id):
    monument = get_object_or_404(Monument, id=monument_id)
    return render(request, 'monument_detail.html', {'monument': monument})

# ----------------------------------✅ Ticket booking------------------------------------------
@login_required
def book_ticket(request, id):
    monument = get_object_or_404(Monument, id=id)
    if request.method == 'POST':
        tickets = int(request.POST.get('tickets', 1))
        booking = Booking.objects.create(user=request.user, monument=monument, tickets=tickets)
        return redirect('create_checkout_session', id=booking.id)
    return render(request, 'book_ticket.html', {'monument': monument})

# -----------------------------------✅ Show bookings-----------------------------------------
@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': bookings})

# -----------------------------------✅ Stripe setup-----------------------------------------
stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request, id):
    booking = get_object_or_404(Booking, id=id)
    YOUR_DOMAIN = 'http://127.0.0.1:8000'

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'unit_amount': 50000,  # ₹500 x 100
                'product_data': {
                    'name': f'{booking.tickets} ticket(s) for {booking.monument.name}',
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=YOUR_DOMAIN + '/payment-success/',
        cancel_url=YOUR_DOMAIN + '/my-bookings/',
    )
    return redirect(session.url, code=303)

def payment_success(request):
    return render(request, 'payment_success.html')

# --------------------------------✅ About & Contact pages-----------------------------------
def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

# ---------------------------------✅ Chatbot response--------------------------------------------------
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        message = data.get('message')
        response_text = "This is a demo response to: " + message
        return JsonResponse({"response": response_text})
    return JsonResponse({"response": "Invalid request."})
