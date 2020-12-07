from .models import Operator, Flight
from .serializers import FlightModelSerializer, OperatorModelSerializer
from .pagination import ModelPageNumberPagination
from .filters import DepartureFilter, ArrivalFilter

from rest_framework import generics, mixins
from rest_framework.filters import SearchFilter, OrderingFilter

from django_filters import rest_framework as filters


class OperatorAPIView(generics.ListCreateAPIView):
    serializer_class = OperatorModelSerializer
    queryset = Operator.objects.all()
    pagination_class = ModelPageNumberPagination
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'name_short')

    #def get(self, request):
     #   return self.list(request)

    #def post(self, request):
     #   return self.create(request)


class OperatorDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OperatorModelSerializer
    queryset = Operator.objects.all()
    lookup_field = 'id'


# storing departures and arrivals as paginated lists
class DeparturesAPIView(generics.ListAPIView):
    serializer_class = FlightModelSerializer
    pagination_class = ModelPageNumberPagination

    # we create a customized queryset
    def get_queryset(self, *args, **kwargs):
        return Flight.objects.filter(line__departure_airport__id=self.kwargs.get('airport_id'))


class ArrivalsAPIView(generics.ListAPIView):
    serializer_class = FlightModelSerializer
    pagination_class = ModelPageNumberPagination

    # we create a customized queryset
    def get_queryset(self, *args, **kwargs):
        return Flight.objects.filter(line__arrival_airport__id=self.kwargs.get('airport_id'))


# filtering and sorting departures and arrivals
class DepartureListAPIView(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightModelSerializer
    pagination_class = ModelPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, )
    filter_class = DepartureFilter
    ordering_fields = ['line__operator', 'line__aircraft', 'line__scheduled_departure', ]
    ordering = 'estimated_delay'


class ArrivalListAPIView(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = FlightModelSerializer
    pagination_class = ModelPageNumberPagination
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, )
    filter_class = ArrivalFilter
    ordering_fields = ['line__operator', 'line__aircraft', 'line__scheduled_arrival', ]
    ordering = 'estimated_delay'
