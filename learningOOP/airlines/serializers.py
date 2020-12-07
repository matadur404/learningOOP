from rest_framework import serializers
from .models import Line, Aircraft, Operator, Flight, Airport


# list of airlines
class OperatorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = '__all__'


# departures and arrivals
class AircraftModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Aircraft
        fields = ('model', )


class AirportLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ('name', )


class OperatorLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operator
        fields = ('name', )


class LineFlightSerializer(serializers.ModelSerializer):
    operator = OperatorLineSerializer()
    departure_airport = AirportLineSerializer()
    arrival_airport = AirportLineSerializer()
    class Meta:
        model = Line
        fields = ('departure_city', 'arrival_city', 'departure_airport', 'arrival_airport', 'scheduled_departure', 'scheduled_arrival', 'operator', )


class FlightModelSerializer(serializers.ModelSerializer):
    line = LineFlightSerializer() # so we can see in depth
    class Meta:
        model = Flight
        fields = ('estimated_delay', 'name_short', 'line', )






