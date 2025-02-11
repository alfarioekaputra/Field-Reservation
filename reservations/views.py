from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, FormView, DetailView
from django.urls import reverse, reverse_lazy

from .forms import ReserVationForm
from .models import Field, TimeSlot, Reservation

class SelectSlotView(FormView):
    template_name = 'reservations/select_slot.html'
    form_class = ReserVationForm
    success_url = 'confirm-reservation/'  # Ganti dengan URL sesuai kebutuhan

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      field_id = self.kwargs['field_id']
      field = get_object_or_404(Field, id=field_id)

      # Ambil tanggal dari request GET
      selected_date = self.request.GET.get('date', None)

      if selected_date:
        # Ambil time slot yang sudah dipesan pada tanggal tersebut
        reserved_slots = Reservation.objects.filter(
          field=field,
          date=selected_date
        ).values_list('time_slots__id', flat=True)

        # Ambil time slot yang tersedia
        if reserved_slots.exists():
          available_slots = TimeSlot.objects.exclude(id__in=reserved_slots)
        else:
          available_slots = TimeSlot.objects.all()

        context['available_slots'] = available_slots
        context['selected_date'] = selected_date

      context['field'] = field
      return context


@login_required  # Pastikan pengguna sudah login
def save_reservation(request, field_id):
    field = get_object_or_404(Field, id=field_id)

    if request.method == 'POST':
        selected_date = request.POST.get('selected_date')
        selected_time_slots = request.POST.getlist('time_slots')

        # Validasi ketersediaan time slot
        reserved_slots = Reservation.objects.filter(
            field=field,
            date=selected_date,
            time_slots__id__in=selected_time_slots
        ).values_list('time_slots__id', flat=True)

        unavailable_slots = set(selected_time_slots).intersection(reserved_slots)
        if unavailable_slots:
            return render(request, 'reservations/error.html', {'message': 'Beberapa time slot tidak tersedia.'})

        # Simpan reservasi
        reservation = Reservation.objects.create(
            user=request.user,
            field=field,
            date=selected_date
        )
        reservation.time_slots.set(selected_time_slots)
        reservation.calculate_total_price()

        return redirect(reverse('confirm_reservation', kwargs={'reservation_id': reservation.id}))

    return redirect('select_slot', field_id=field_id)


class ConfirmReservationView(DetailView):
  model = Reservation
  template_name = 'reservations/confirm_reservation.html'
  context_object_name = 'reservation'

  def get_object(self, queryset=None):
    reservation_id = self.kwargs['reservation_id']
    return get_object_or_404(Reservation, id=reservation_id)