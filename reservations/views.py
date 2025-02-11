from django.shortcuts import get_object_or_404, redirect
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


    def form_valid(self, form):
      field_id = self.kwargs['field_id']
      field = get_object_or_404(Field, id=field_id)
      selected_date = self.request.GET.get('date')
      selected_time_slots = self.request.POST.getlist('time_slots')

      print("Selected Date:", selected_date)  # Debugging
      print("Selected Time Slots:", selected_time_slots)  # Debugging

      # Validasi ketersediaan time slot
      reserved_slots = Reservation.objects.filter(
        field=field,
        date=selected_date,
        time_slots__id__in=selected_time_slots
      ).values_list('time_slots__id', flat=True)

      print("reserved_slots:", reserved_slots)  # Debugging

      unavailable_slots = set(selected_time_slots).intersection(reserved_slots)
      if unavailable_slots:
        form.add_error(None, 'Beberapa time slot tidak tersedia.')
        return self.form_invalid(form)

      # Simpan reservasi sementara
      reservation = Reservation.objects.create(
        user=self.request.user,
        field=field,
        date=selected_date
      )
      reservation.time_slots.set(selected_time_slots)
      reservation.calculate_total_price()

      self.success_url = reverse_lazy('confirm_reservation', kwargs={'reservation_id': reservation.id})
      return super().form_valid(form)


class ConfirmReservationView(DetailView):
  model = Reservation
  template_name = 'reservations/confirm_reservation.html'
  context_object_name = 'reservation'

  def get_object(self, queryset=None):
    reservation_id = self.kwargs['reservation_id']
    return get_object_or_404(Reservation, id=reservation_id)