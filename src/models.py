from django.db import models

class Program(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

class Apartment(models.Model):
    surface = models.FloatField()
    price = models.FloatField()
    number_of_rooms = models.IntegerField()
    caracteristics = models.CharField(max_length=255)
    program = models.ForeignKey(Program,related_name='Apartments',on_delete=models.CASCADE)
