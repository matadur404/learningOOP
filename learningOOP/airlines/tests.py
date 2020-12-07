from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Operator, Country, City, Airport, Line, Aircraft, Flight, Manufacturer, PlaneModel
import json


class CountryTest(APITestCase):

    def setUp(self):
        self.country = Country.objects.create(name='Greece', name_short='GR')

    def test_create_country(self):
        self.assertIs(self.country.name, 'Greece')
        self.assertIs(self.country.name_short, 'GR')


class CityTest(APITestCase):

    def setUp(self):
        self.country = Country.objects.create(name='Greece', name_short='GR')
        self.city = City.objects.create(name='Patra', name_short='PA', country=self.country)

    def test_relationship_fk_city_country(self):
        self.assertIs(self.city.country, self.country)


class OperatorAPITest(APITestCase):

    def setUp(self):
        self.url = reverse('operator')
        self.country = Country.objects.create(name='Greece', name_short='GR')
        self.city = City.objects.create(name='Athens', name_short='ATH', country=self.country)
        self.airport = Airport.objects.create(name='Elefterios Venizelos', name_short='EV', city=self.city)
        self.data = {'name': 'Olympic Air',
                    'name_short': 'OA',
                    'country_of_origin': self.country.pk,
                    'airport': [self.airport.pk]}

    def test_create_operator(self):
        data = self.data
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Operator.objects.count(), 1)
        self.assertEqual(Operator.objects.get().name, 'Olympic Air')

    def test_create_operator_no_data(self):
        data = {}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Operator.objects.count(), 0)

    def test_create_operator_wrong_data(self):
        data = {'name': 'Blabla',
                'name_short': 'BLA',
                'country_of_origin': 'Oz',
                'airport': 'Wizard'}
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_operator_missing_data(self):
        data = self.data
        del data['airport']
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_operator_missing_data_with_default_value(self):
        data = self.data
        del data['name']
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_operator(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_operator_methods_not_allowed(self):
        methods_not_allowed = ['PUT', 'PATCH', 'DELETE']
        for method in methods_not_allowed:
            response = getattr(self.client, method.lower())(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class OperatorDetailAPITest(APITestCase):

    def setUp(self):
        self.country = Country.objects.create(name='Greece', name_short='GR')
        self.city = City.objects.create(name='Athens', name_short='ATH', country=self.country)
        self.airport = Airport.objects.create(name='Elefterios Venizelos', name_short='EV', city=self.city)
        self.operator = Operator.objects.create(name='Olympic Air', name_short='OA', country_of_origin=self.country)
        self.operator.airport.add(self.airport)

    def test_operator_detail_retrieve(self):
        response = self.client.get(reverse('operator/id', kwargs={'id': self.operator.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Operator.objects.count(), 1)
        self.assertEqual(Operator.objects.get().name, 'Olympic Air')

    def test_operator_detail_retrieve_wrong_id(self):
        response = self.client.get(reverse('operator/id', kwargs={'id': 66}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_operator_detail_put(self):
        response = self.client.put(reverse('operator/id', kwargs={'id': self.operator.id}),
                                   {'name': 'Aegean',
                                    'name_short': 'GR',
                                    'country_of_origin': self.country.pk, # int because it is a foreign key!
                                    'airport': [self.airport.pk]}) # list because it is a many to many relationship
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {'id': self.operator.id,
                          'name': 'Aegean',
                          'name_short': 'GR',
                          'country_of_origin': self.country.pk,
                          'airport': [self.airport.pk]})

    def test_operator_detail_patch(self):
        response = self.client.patch(reverse('operator/id', kwargs={'id': self.operator.id}),
                                     {'name': 'SmartWings'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content),
                         {'id': self.operator.id,
                          'name': 'SmartWings',
                          'name_short': 'OA',
                          'country_of_origin': self.country.pk,
                          'airport': [self.airport.pk]})

    def test_operator_detail_delete(self):
        response = self.client.delete(reverse('operator/id', kwargs={'id': self.operator.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Operator.objects.count(), 0)

    def test_operator_detail_delete_wrong_id(self):
        response = self.client.delete(reverse('operator/id', kwargs={'id': 66}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Operator.objects.count(), 1)


class DeparturesAPITest(APITestCase):

    def setUp(self):
        self.url = reverse('departures')
        self.country = Country.objects.create(name='Greece', name_short='GR')
        self.departure_city = City.objects.create(name='Athens', name_short='ATH', country=self.country)
        self.arrival_city = City.objects.create(name='Patras', name_short='PT', country=self.country)
        self.departure_airport = Airport.objects.create(name='Elefterios Venizelos',
                                                        name_short='EV',
                                                        city=self.departure_city)
        self.arrival_airport = Airport.objects.create(name='Kapio Aerodromio', name_short='KA', city=self.arrival_city)
        self.operator = Operator.objects.create(name='Olympic Air', name_short='OA', country_of_origin=self.country)
        self.manufacturer = Manufacturer.objects.create(name='Airbus', name_short='AB')
        self.plane_model = PlaneModel.objects.create(name='Airbus100',
                                                     name_short='AB100',
                                                     manufacturer=self.manufacturer,
                                                     capacity=500)
        self.aircraft = Aircraft.objects.create(name='Airbus',
                                                name_short='AB',
                                                model=self.plane_model,
                                                operator=self.operator)

        self.data_line = {
            'aircraft': self.aircraft,
            'operator': self.operator,
            'departure_airport': self.departure_airport,
            'arrival_airport': self.arrival_airport,
            'departure_city': self.departure_city,
            'arrival_city': self.arrival_city,
            'scheduled_departure': '10:27:48',
            'scheduled_arrival': '23:34:45'
        }
        self.line = Line.objects.create(**self.data_line)

        self.data_flight = {
            'name': 'Flight',
            'name_short': 'FL7538',
            'line': self.line,
            'distance': 5000,
            'estimated_delay': 2,
            'real_delay': 1,
            'passengers': 506
        }
        self.flight = Flight.objects.create(**self.data_flight)

    def test_departures_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(json.loads(response.content)['results']), 1)

    def test_departures_get_wrong_id(self):
        response = self.client.get('/airport/66/departures/')
        self.assertEquals(len(json.loads(response.content)["results"]), 0)

    def test_departures_methods_not_allowed(self):
        methods_not_allowed = ['PUT', 'PATCH', 'DELETE']
        for method in methods_not_allowed:
            response = getattr(self.client, method.lower())(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class DArrivalsAPITest(APITestCase):

    def setUp(self):
        self.url = reverse('arrivals')
        self.country = Country.objects.create(name='Greece', name_short='GR')
        self.departure_city = City.objects.create(name='Athens', name_short='ATH', country=self.country)
        self.arrival_city = City.objects.create(name='Patras', name_short='PT', country=self.country)
        self.departure_airport = Airport.objects.create(name='Elefterios Venizelos',
                                                        name_short='EV',
                                                        city=self.departure_city)
        self.arrival_airport = Airport.objects.create(name='Kapio Aerodromio', name_short='KA', city=self.arrival_city)
        self.operator = Operator.objects.create(name='Olympic Air', name_short='OA', country_of_origin=self.country)
        self.manufacturer = Manufacturer.objects.create(name='Airbus', name_short='AB')
        self.plane_model = PlaneModel.objects.create(name='Airbus100',
                                                     name_short='AB100',
                                                     manufacturer=self.manufacturer,
                                                     capacity=500)
        self.aircraft = Aircraft.objects.create(name='Airbus',
                                                name_short='AB',
                                                model=self.plane_model,
                                                operator=self.operator)

        self.data_line = {
            'aircraft': self.aircraft,
            'operator': self.operator,
            'departure_airport': self.departure_airport,
            'arrival_airport': self.arrival_airport,
            'departure_city': self.departure_city,
            'arrival_city': self.arrival_city,
            'scheduled_departure': '10:27:48',
            'scheduled_arrival': '23:34:45'
        }
        self.line = Line.objects.create(**self.data_line)

        self.data_flight = {
            'name': 'Flight',
            'name_short': 'FL7538',
            'line': self.line,
            'distance': 5000,
            'estimated_delay': 2,
            'real_delay': 1,
            'passengers': 506
        }
        self.flight = Flight.objects.create(**self.data_flight)

    def test_departures_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(len(json.loads(response.content)['results']), 1)

    def test_departures_get_wrong_id(self):
        response = self.client.get('/airport/66/departures/')
        self.assertEquals(len(json.loads(response.content)["results"]), 0)

    def test_departures_methods_not_allowed(self):
        methods_not_allowed = ['PUT', 'PATCH', 'DELETE']
        for method in methods_not_allowed:
            response = getattr(self.client, method.lower())(self.url)
            self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
