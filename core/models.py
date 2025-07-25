from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# --- Existing Monument model ---
class Monument(models.Model):
    CATEGORY_CHOICES = [
        ('Monument', 'Monument'),
        ('Museum', 'Museum'),
        ('Park', 'Park'),
    ]

    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    price_per_ticket = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='monuments/')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Monument')

    def __str__(self):
        return self.name

# --- Existing Booking model ---
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monument = models.ForeignKey(Monument, on_delete=models.CASCADE)
    date = models.DateField()
    num_tickets = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.monument.name} on {self.date}"

# --- Existing MonumentImage model ---
class MonumentImage(models.Model):
    monument = models.ForeignKey(Monument, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='monuments/extra_images/')

    def __str__(self):
        return f"Image of {self.monument.name}"

# --- ✅ New Profile model for phone, OTP, is_verified ---
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile of {self.user.username}"

# --- Auto-create or update Profile on User save ---
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        instance.profile.save()
