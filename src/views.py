import json

from django.http.response import JsonResponse
from django.db.models import Q
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from src.serializers import ApartmentSerializer, ApartmentPostSerializer, ProgramSerializer
from src.models import Apartment, Program
from rest_framework import generics
from django.core import serializers


class ApartmentView(APIView):

    def get(self, request):
        apartments = Apartment.objects.all()
        apartments_serializer = ApartmentSerializer(apartments, many=True)

        for apartment in apartments_serializer.data:
            apartment['caracteristics'] = apartment['caracteristics'].split(
                '|')
        return JsonResponse(apartments_serializer.data, safe=False)

    def post(self, request):

        payload = JSONParser().parse(request)

        program = Program.objects.filter(pk=payload['program'])
        if not program:
            return JsonResponse("Program not found",
                                status=status.HTTP_404_NOT_FOUND,
                                safe=False)

        payload['caracteristics'] = "|".join(
            payload['caracteristics'])

        apartment_serializer = ApartmentPostSerializer(data=payload)

        if apartment_serializer.is_valid():
            apartment_serializer.save()
            return JsonResponse('OK', status=status.HTTP_200_OK,
                                safe=False)
        else:
            return JsonResponse(apartment_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST,
                                safe=False)


class ApartmentListActivePrograms(generics.ListAPIView):
    serializer_class = ApartmentSerializer

    def get_queryset(self):
       return Apartment.objects.filter(program__is_active=True)


class ApartmentListPriceBetween(generics.ListAPIView):
    serializer_class = ApartmentSerializer

    def get_queryset(self):
       return Apartment.objects.filter(
           Q(price__gte=100) & Q(price__lte=180))


class ApartmentListPromoCode(generics.ListAPIView):
    serializer_class = ApartmentSerializer

    def get_queryset(self):

        apartments = Apartment.objects.all()
        apartments_serializer = ApartmentSerializer(apartments, many=True)
        promo_code = self.kwargs.get('promo_code')

        response = []
        if promo_code == 'PERENOEL':

            for apartment in apartments_serializer.data:
                new_appartment = apartment
                new_appartment['price'] = round(
                    new_appartment['price'] * 0.95, 3)
                new_appartment['program']['name'] = f"{new_appartment['program']['name']} PROMO SPECIALE"
                response.append(new_appartment)

            return response
        else:
            return apartments


class ProgramList(generics.ListAPIView):
   serializer_class = ProgramSerializer

   def get_queryset(self):

       return Program.objects.filter(Apartments__caracteristics__contains='swimming pool').distinct()
