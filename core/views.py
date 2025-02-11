from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from reservations.models import Field

# Create your views here.
def user_login(request):
    template_name = 'core/login.html'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        print("user", username)
        print("user", password)
        if user is not None:
            print("User authenticated:", user.username)
            login(request, user)  # Login pengguna
            next_url = request.GET.get('next', '/')  # Redirect ke halaman sebelumnya
            return redirect(next_url)
        else:
            print("Authentication failed")
            error_message = "Username atau password salah."
            return render(request, template_name, {'error_message': error_message})

    return render(request, template_name)

def logout_user(request):
    logout(request)
    return redirect('home')

def home(request):
    fields = Field.objects.all()
    return render(request, 'core/home.html', {'fields': fields})