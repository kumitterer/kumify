"""kumify URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from msgio.views import TelegramWebhookView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', include('profiles.urls', 'profiles')),
    path('', include("frontend.urls", "frontend")),
    path('mood/', include("mood.urls", "mood")),
    path('cron/', include("cronhandler.urls", "cron")),
    path('webhooks/telegram/', TelegramWebhookView.as_view()),
    path('dreams/', include("dreams.urls", "dreams")),
    path('gpslog/', include("gpslog.urls")),
    path('oidc/', include('mozilla_django_oidc.urls')),
]
