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

   program_id = serializers.IntegerField(source='program.id')
   program_name = serializers.CharField(source='program.name')
   class Meta:
       model = Apartment
       fields =  ('pk','program_id','program_name','surface','price','number_of_rooms','caracteristics')

class ApartmentPostSerializer(serializers.ModelSerializer):

   class Meta:
       model = Apartment
       fields =  ('pk','program','surface','price','number_of_rooms','caracteristics')

class ApartmentPromoSerializer(serializers.ModelSerializer):
    new_price = serializers.FloatField()
    program_id = serializers.IntegerField(source='program.id')
    program_name = serializers.CharField(source='program.name')
    label = serializers.CharField()

    class Meta:
        model = Apartment
        fields = ('pk','price' ,'new_price','program_id','program_name','label','surface')