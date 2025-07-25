from django.shortcuts import render, get_object_or_404, redirect
from .models import Monument, Booking
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from decimal import Decimal
from datetime import date
from django.conf import settings
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages


stripe.api_key = settings.STRIPE_SECRET_KEY

from django.db.models import Prefetch
from .models import Monument, MonumentImage

def home(request):
    query = request.GET.get('q')

    # Fetch monuments with related images using prefetch
    base_qs = Monument.objects.prefetch_related(
        Prefetch('images', queryset=MonumentImage.objects.all())
    )

    if query:
        base_qs = base_qs.filter(name__icontains=query)

    # Categorize the monuments
    monuments_by_category = {
        'Monuments': base_qs.filter(category='Monument'),
        'Museums': base_qs.filter(category='Museum'),
        'Parks': base_qs.filter(category='Park'),
    }

    return render(request, 'home.html', {
        'monuments_by_category': monuments_by_category,
        'query': query
    })



from .models import Monument, MonumentImage

def monument_detail(request, monument_id):
    monument = Monument.objects.get(pk=monument_id)
    images = monument.images.all()  # This will fetch related MonumentImage objects
    return render(request, 'monument_detail.html', {
        'monument': monument,
        'images': images,
    })





@login_required
def book_ticket(request, id):
    monument = get_object_or_404(Monument, id=id)

    if request.method == 'POST':
        num_tickets = int(request.POST['num_tickets'])
        visit_date = request.POST['visit_date']
        total = Decimal(monument.price_per_ticket) * num_tickets

        # Save booking data to session for later
        request.session['booking_data'] = {
            'monument_id': monument.id,
            'visit_date': visit_date,
            'num_tickets': num_tickets,
            'total': float(total)
        }

        return redirect('create_checkout_session', id=monument.id)

    return render(request, 'book_ticket.html', {
        'monument': monument,
        'publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })


@csrf_exempt
@login_required
def create_checkout_session(request, id):
    monument = get_object_or_404(Monument, id=id)
    data = request.session.get('booking_data')
    if not data:
        return redirect('home')

    total = int(data['total'] * 100)  # Stripe expects amount in paise
    YOUR_DOMAIN = "http://127.0.0.1:8000"

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'inr',
                    'unit_amount': total,
                    'product_data': {
                        'name': monument.name,
                    },
                },
                'quantity': data['num_tickets'],
            }],
            mode='payment',
            success_url=YOUR_DOMAIN + '/payment-success/',
            cancel_url=YOUR_DOMAIN + '/',
        )
        return redirect(checkout_session.url, code=303)

    except Exception as e:
        return JsonResponse({'error': str(e)})


@login_required
def payment_success(request):
    data = request.session.get('booking_data')
    if not data:
        return redirect('home')

    monument = get_object_or_404(Monument, id=data['monument_id'])

    Booking.objects.create(
        user=request.user,
        monument=monument,
        date=data['visit_date'],
        num_tickets=data['num_tickets'],
        total_amount=data['total'],
        payment_status=True
    )

    del request.session['booking_data']

    return render(request, 'payment_success.html')


from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Booking

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-date')
    context = {
        'bookings': bookings
    }
    return render(request, 'my_bookings.html', context)





from google.protobuf.json_format import MessageToDict
from google.oauth2 import service_account
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
import uuid
from google.cloud import dialogflow_v2 as dialogflow
from django.conf import settings

@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        try:
            # Read JSON from fetch
            data = json.loads(request.body)
            user_message = data.get('message')

            # Load Dialogflow credentials
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(settings.BASE_DIR, 'dialogflow_key.json')

            # Setup Dialogflow session
            session_client = dialogflow.SessionsClient()
            session = session_client.session_path('ticket-trivia-chatbot', str(uuid.uuid4()))

            text_input = dialogflow.TextInput(text=user_message, language_code='en')
            query_input = dialogflow.QueryInput(text=text_input)

            # Get response from Dialogflow
            response = session_client.detect_intent(session=session, query_input=query_input)
            chatbot_reply = response.query_result.fulfillment_text

            return JsonResponse({'reply': chatbot_reply})

        except Exception as e:
            logging.error(f"Dialogflow Error: {e}")
            return JsonResponse({'reply': "Sorry, something went wrong. 😢"})
        

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

import random
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.mail import send_mail
from .forms import EmailForm, OTPForm
from .models import Profile

def send_otp(email):
    return str(random.randint(100000, 999999))

def signup_email_view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user, created = User.objects.get_or_create(username=email, email=email)
            otp = send_otp(email)
            profile = user.profile
            profile.otp = otp
            profile.save()

            send_mail(
                subject='Your OTP for Ticket Trivia',
                message=f'Your OTP is {otp}',
                from_email='youremail@example.com',
                recipient_list=[email],
                fail_silently=False,
            )
            request.session['email'] = email
            return redirect('verify_otp')
    else:
        form = EmailForm()
    return render(request, 'signup_email.html', {'form': form})


def verify_otp_view(request):
    email = request.session.get('email')
    if not email:
        return redirect('signup_email')

    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            otp = form.cleaned_data['otp']
            user = User.objects.filter(email=email).last()  # ✅ gets the most recent match

            if user.profile.otp == otp:
                user.profile.is_verified = True
                user.profile.otp = ''
                user.profile.save()
                login(request, user)
                messages.success(request, "OTP verified and login successful! ✅")
                return redirect('home')

            else:
                form.add_error('otp', 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})


from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django import forms
import random
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import Profile

# Signup Forms
class SignupForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

class OtpForm(forms.Form):
    otp = forms.CharField(label="Enter OTP", max_length=6)

def signup_view(request):
    show_otp = False
    if request.method == 'POST':
        if 'otp' in request.POST:
            # OTP entered
            otp_form = OtpForm(request.POST)
            form = SignupForm(request.session['signup_data'])
            if otp_form.is_valid() and form.is_valid():
                user_otp = otp_form.cleaned_data['otp']
                email = form.cleaned_data['email']
                profile = Profile.objects.filter(email=email).last()
                if profile and profile.otp == user_otp:
                    user = User.objects.create_user(
                        username=form.cleaned_data['username'],
                        email=email,
                        password=form.cleaned_data['password']
                    )
                    profile.user = user
                    profile.save()
                    login(request, user)
                    messages.success(request, "Account created successfully! 🎉")
                    return redirect('home')  # or '/'

                else:
                    otp_form.add_error('otp', 'Invalid OTP')
            show_otp = True
        else:
            # Initial form submitted
            form = SignupForm(request.POST)
            otp_form = OtpForm()
            if form.is_valid():
                email = form.cleaned_data['email']
                otp = str(random.randint(100000, 999999))
                Profile.objects.create(email=email, otp=otp)
                send_mail(
                    subject='Your OTP for Ticket Trivia Signup',
                    message=f'Your OTP is {otp}',
                    from_email=None,
                    recipient_list=[email],
                    fail_silently=False
                )
                request.session['signup_data'] = request.POST
                show_otp = True
    else:
        form = SignupForm()
        otp_form = OtpForm()
    return render(request, 'signup.html', {
        'form': form,
        'otp_form': otp_form,
        'show_otp': show_otp
    })
