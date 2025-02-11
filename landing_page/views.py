from django.shortcuts import render

from reservations.models import Field


# Create your views here.
def home(request):
    fields = Field.objects.all()
    return render(request, 'landing_page/home.html', {'fields': fields})