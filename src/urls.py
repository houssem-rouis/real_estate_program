from django.urls import path
from src.views import ApartmentView



urlpatterns = [

    path('apartments/', ApartmentView.as_view(), name=""),

]
