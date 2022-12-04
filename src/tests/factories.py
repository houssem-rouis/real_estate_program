import factory
from src.models import Apartment , Program


class AparmtentFactory(factory.Factory):

    surface = factory.Faker("150")
    price = factory.Faker('180')
    caracteristics = factory.Faker('swimming_pool')
    number_of_rooms = factory.Faker('5')

    class Meta:
        model = Apartment