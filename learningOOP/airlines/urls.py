from django.urls import path
from . import views


urlpatterns = [
    path('operator/', views.OperatorAPIView.as_view(), name='operator'),
    path('operator/<int:id>', views.OperatorDetailAPIView.as_view(), name='operator/id'),
    path('airport/<int:airport_id>/departures/', views.DeparturesAPIView.as_view()),
    path('airport/<int:airport_id>/arrivals/', views.ArrivalsAPIView.as_view()),
    path('departures/', views.DepartureListAPIView.as_view(), name='departures'),
    path('arrivals/', views.ArrivalListAPIView.as_view(), name='arrivals'),
]