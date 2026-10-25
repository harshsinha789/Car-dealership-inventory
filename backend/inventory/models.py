from django.conf import settings
from django.db import models
class Vehicle(models.Model):
    CATEGORY_CHOICES = [('sedan','Sedan'),('suv','SUV'),('hatchback','Hatchback'),('coupe','Coupe'),('truck','Truck'),('other','Other')]
    make = models.CharField(max_length=80)
    model = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    price = models.DecimalField(max_digits=12, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta: ordering = ['make','model']
    def __str__(self): return f'{self.make} {self.model}'
class Purchase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    purchased_at = models.DateTimeField(auto_now_add=True)
