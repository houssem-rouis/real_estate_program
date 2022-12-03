from django.urls import path
from src.views import ApartmentView ,ApartmentListPromoCode



urlpatterns = [
    path('apartmentslist/<str:promo_code>', ApartmentListPromoCode.as_view()),

    path('apartments/', ApartmentView.as_view(), name=""),

]
