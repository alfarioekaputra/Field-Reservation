"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings 
from django.conf.urls.static import static
from django.urls import path, include

from reservations.views import ConfirmReservationView, SelectSlotView, save_reservation
from core.views import user_login, logout_user

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('field/<int:field_id>/select-slot/', SelectSlotView.as_view(), name='select_slot'),
    path('field/<int:field_id>/save-reservation/', save_reservation, name='save_reservation'),
    path('reservation/<int:reservation_id>/confirm/', ConfirmReservationView.as_view(), name='confirm_reservation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
