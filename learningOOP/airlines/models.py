from django.db import models


class MainModel(models.Model):
    name = models.CharField(max_length=50, default='name')
    name_short = models.CharField(max_length=10, default='n')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


class Manufacturer(MainModel):
    pass


class PlaneModel(MainModel):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='models')
    capacity = models.PositiveIntegerField()


class Aircraft(MainModel):
    model = models.ForeignKey(PlaneModel, on_delete=models.CASCADE, related_name='aircrafts')
    operator = models.ForeignKey('Operator', on_delete=models.CASCADE, related_name='aircrafts')


class Country(MainModel):
    pass


class City(MainModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='cities')


class Airport(MainModel):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='airports')


class Operator(MainModel):
    country_of_origin = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='operators')
    airport = models.ManyToManyField(Airport)


class Line(models.Model):
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name='lines')
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, related_name='lines')
    departure_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_lines')
    arrival_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival_lines')
    departure_city = models.CharField(max_length=20)
    arrival_city = models.CharField(max_length=20)
    scheduled_departure = models.TimeField(auto_now=False, auto_now_add=False)
    scheduled_arrival = models.TimeField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return f"{self.departure_city} -{self.arrival_city}"


class Flight(MainModel):
    """use name_short for flight number"""
    line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name='flights')
    distance = models.PositiveIntegerField()
    estimated_delay = models.IntegerField()
    real_delay = models.IntegerField()
    passengers = models.PositiveIntegerField()
