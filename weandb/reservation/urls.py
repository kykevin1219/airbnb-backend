from django.urls import path
from .views import ReservationView, ReservationListView, ReservationHostView, ConfirmView

urlpatterns = [
    path('', ReservationView.as_view()),
    path('/list', ReservationListView.as_view()),
    path('/host', ReservationHostView.as_view()),
    path('/confirm', ConfirmView.as_view()),
]
