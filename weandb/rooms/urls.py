from django.urls import path
from .views import RoomView, DetailView, RandomRecommendationView, CityRecommendationView, SearchView, CitySearchView

urlpatterns = [
    path('', RoomView.as_view()),
    path('/<int:room_no>', DetailView.as_view()),
    path('/cityrecommendation', RandomRecommendationView.as_view()),
    path('/cities', CityRecommendationView.as_view()),
    path('/cities/<int:city_no>', CitySearchView.as_view()),
    path('/search', SearchView.as_view())
]
