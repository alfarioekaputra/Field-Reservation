import path
from django.urls import path

from core.views import home, user_login, logout_user

urlpatterns = [
    path('login/', user_login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('', home, name='home'),
]