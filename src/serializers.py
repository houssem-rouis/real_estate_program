from rest_framework import serializers

from src.models import Apartment , Program

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
      model = Program
      fields = ('id', 'name')

class ProgramReadSerializer(serializers.ModelSerializer):
    class Meta:
      model = Program
      fields = ('id',)

class ApartmentSerializer(serializers.ModelSerializer):
   program = ProgramSerializer()

   class Meta:
       model = Apartment
       fields =  ('pk','program','surface','price','number_of_rooms','caracteristics')

class ApartmentPostSerializer(serializers.ModelSerializer):

   class Meta:
       model = Apartment
       fields =  ('pk','program','surface','price','number_of_rooms','caracteristics')