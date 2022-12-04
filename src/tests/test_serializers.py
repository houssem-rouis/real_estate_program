from django.test import TestCase

from src.serializers import ApartmentSerializer
from src.tests.factories import AparmtentFactory


class ApartmentSerializer(TestCase):
    def test_model_fields(self):

        appartment = AparmtentFactory()
        serializer = ApartmentSerializer()
        for field_name in [
            'id', 'program_id', 'program_name', 'surface', 'number_of_rooms', 'caracteristics'
        ]:
            self.assertEqual(
                serializer.data[field_name],
                getattr(appartment, field_name)
            )