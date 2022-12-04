import datetime

from django.http.response import JsonResponse
from django.db.models import Q, F
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from src.serializers import ApartmentPromoSerializer, ApartmentSerializer, ApartmentPostSerializer, ProgramSerializer
from src.models import Apartment, Program
from rest_framework import generics
from django.db.models import Value, CharField , Case, When, Value, IntegerField

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


class ApartmentViewQueries(APIView):
    serializer_class = ApartmentSerializer

    def get_active_program_appartments(request):
        return Apartment.objects.filter(program__is_active=True)

    def get_programs_price_between(request):
        return Apartment.objects.filter(
            Q(price__gte=100) & Q(price__lte=180))

    def list_progrmas_promo_code(self):

        promo_code = self.kwargs.get('promo_code')

        if promo_code == 'PERE NOEL':
            return Apartment.objects.annotate(new_price=F('price') * 0.95).annotate(label=Value('PROMO SPECIALE', output_field=CharField()))
        else:
            return Apartment.objects.all()

    def list_appartments_by_season(self):
        current_month = datetime.datetime.now().month

        if current_month in [6, 7, 8, 9]:
            return Apartment.objects.annotate(
                custom_order=Case(
                    When(caracteristics__contains="swimming pool", then=Value(1)),
                    When(caracteristics__notcontains="swimming pool", then=Value(2)),
                    output_field=IntegerField(),
                )
            ).order_by('custom_order', '-price', '-surface')
        elif current_month in [12, 1, 2, 3]:
            return Apartment.objects.annotate(
                custom_order=Case(
                    When(caracteristics__contains="near ski resort", then=Value(1)),
                    When(caracteristics__notcontains="near ski resort",
                         then=Value(2)),
                    output_field=IntegerField(),
                )
            ).order_by('custom_order', '-price', '-surface')
        else:
            return Apartment.objects.all().order_by('-price', '-surface')


class ProgramList(generics.ListAPIView):
   serializer_class = ProgramSerializer

   def programs_with_swimming_pool(self):

       return Program.objects.filter(Apartments__caracteristics__contains='swimming pool').distinct()
