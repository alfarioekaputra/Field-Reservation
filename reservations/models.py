from django.db import models

# Create your models here.
class Field(models.Model):
  name = models.CharField(max_length=100)
  type = models.CharField(max_length=50)
  price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
  image = models.ImageField(upload_to='images/')

  def __str__(self):
    return self.name
  
class TimeSlot(models.Model):
  start_time = models.TimeField()
  end_time = models.TimeField()

  def __str__(self):
    return f'{self.start_time} to {self.end_time}'

class Reservation(models.Model):
  user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
  field = models.ForeignKey(Field, on_delete=models.CASCADE)
  date = models.DateField()
  time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
  total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  status = models.CharField(max_length=50, default='pending')

  def calculate_total_price(self):
    duration_hours = self.time_slot.count() # hitung jumlah time slot
    self.total_price = self.field.price_per_hour * duration_hours
    self.save()

  def __str__(self):
    return f'{self.user.username} on {self.field.name} at {self.date}'