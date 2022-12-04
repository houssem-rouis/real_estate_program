
import pytest
from django.test import TestCase
from src.models import Apartment, Program
import pytest
from freezegun import freeze_time
from src.views import ApartmentPromoCode, ApartmentViewQueries, ProgramList


class ViewTest(TestCase):
    def setUp(self):
        program = Program.objects.create(id=1, name="prog1", is_active=False)
        program_2 = Program.objects.create(id=2, name="prog2", is_active=True)
        program_3 = Program.objects.create(id=3, name="prog3", is_active=False)
        Apartment.objects.create(id=1, surface=100, price=150, number_of_rooms=5,
                                 caracteristics='near ski resort', program=program)
        Apartment.objects.create(id=2, surface=150, price=180, number_of_rooms=7,
                                 caracteristics='swimming pool | cave', program=program)
        Apartment.objects.create(id=3, surface=220, price=250, number_of_rooms=9,
                                 caracteristics='near ski resort | garden', program=program)
        Apartment.objects.create(id=4, surface=200, price=250, number_of_rooms=9,
                                 caracteristics='swimming pool | american style', program=program_2)
        Apartment.objects.create(id=5, surface=100, price=110, number_of_rooms=4,
                                 caracteristics='cave | garden', program=program_3)

    @pytest.mark.django_db
    def test_get_all_apartments(self):

        response = self.client.get("/src/apartments", follow=True)
        assert response.status_code == 200

        expected_appartments = [{'caracteristics': ['near ski resort'], 'number_of_rooms': 5, 'pk': 1, 'price': 150.0, 'surface':100, 'program_name':'prog1', 'program_id':1},
                                {'caracteristics': ['swimming pool ', ' cave'], 'number_of_rooms': 7, 'pk': 2,
                                    'price': 180.0, 'surface':150, 'program_name':'prog1', 'program_id':1},
                                {'caracteristics': ['near ski resort ', ' garden'], 'number_of_rooms': 9,
                                    'pk': 3, 'price': 250.0, 'surface':220, 'program_name':'prog1', 'program_id':1},
                                {'caracteristics': ['swimming pool ', ' american style'], 'number_of_rooms': 9,
                                    'pk': 4, 'price': 250.0, 'surface':200, 'program_name':'prog2', 'program_id':2},
                                {'caracteristics': ['cave ', ' garden'], 'number_of_rooms': 4, 'pk': 5, 'price': 110.0, 'surface':100, 'program_name':'prog3', 'program_id':3}]
        response_appartments = response.json()

        assert len(response_appartments) == 5
        for count, appartment in enumerate(response_appartments):
            assert expected_appartments[count] == appartment

    @pytest.mark.django_db
    def test_get_active_programs_apartments(self):

        apartments = ApartmentViewQueries.get_active_program_appartments()
        assert len(apartments) == 1
        assert apartments[0].id == 4

    @pytest.mark.django_db
    def test_get_active_programs_apartments(self):

        apartments = ApartmentViewQueries.get_programs_price_between()
        assert len(apartments) == 3

        assert [apartment.id for apartment in apartments] == [1, 2, 5]

    @pytest.mark.django_db
    def test_list_apartments_with_promo_code(self):

        promo_code = "PERE NOEL"

        apartments = ApartmentPromoCode.list_program_promo_code(promo_code)

        assert len(apartments) == 5

        assert [apartment.new_price for apartment in apartments] == [142.5, 171.0,237.5,237.5,104.5]

        assert apartments[0].label == "PROMO SPECIALE"

    @pytest.mark.django_db
    def test_list_apartments_without_promo_code(self):

        promo_code = ""

        apartments = ApartmentPromoCode.list_program_promo_code(promo_code)

        assert len(apartments) == 5

        with pytest.raises(AttributeError):
            new_prices = [apartment.new_price for apartment in apartments]

        with pytest.raises(AttributeError):
            labels = [apartment.new_price for apartment in apartments]

    @freeze_time("2022-10-01 00:00:00")
    @pytest.mark.django_db
    def test_list_apartments_by_season_other(self):

        apartments = ApartmentViewQueries.list_appartments_by_season()

        assert [apartment.id for apartment in apartments] == [3, 4, 2, 1, 5]

    @freeze_time("2022-07-01 00:00:00")
    @pytest.mark.django_db
    def test_list_apartments_by_season_summer(self):

        apartments = ApartmentViewQueries.list_appartments_by_season()

        assert [apartment.id for apartment in apartments] == [4, 2, 3, 1, 5]

    @freeze_time("2022-01-01 00:00:00")
    @pytest.mark.django_db
    def test_list_apartments_by_season_winter(self):

        apartments = ApartmentViewQueries.list_appartments_by_season()

        assert [apartment.id for apartment in apartments] == [3, 1, 4, 2, 5]

    @pytest.mark.django_db
    def test_list_programs_with_apartements_having_swimming_pool(self):

        programs = ProgramList.programs_with_swimming_pool()

        assert [program.id for program in programs] == [1, 2]
