from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views  # ✅ already imported

urlpatterns = [
    path('admin/', admin.site.urls),

    # ✅ Show signup/login page on homepage
    path('', core_views.signup_email_view, name='signup_email'),

    # ✅ Include other URLs from core app
    path('core/', include('core.urls')),
]

# ✅ Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)








