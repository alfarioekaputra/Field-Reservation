from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.html import format_html

from reservations.models import Field, TimeSlot


# Register your models here.
@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
  def image_tag(self):
    return mark_safe('<img src="%s" width ="50" height="50"/>'%(self.image.url))
  
  def price_per_hour2(self, obj):
    return f'Rp. {obj.price_per_hour}'
  
  def image_tag(self, obj):
    return format_html('<img src="{}" style="max-width:200px; max-height:200px"/>'.format(obj.image.url))

  
  fields = ['name', 'type', 'price_per_hour', 'image']
  list_display = ['name', 'type', 'price_per_hour2', 'image_tag']

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
  pass
