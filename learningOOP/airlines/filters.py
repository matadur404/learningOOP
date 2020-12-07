import django_filters as df
from .models import Line, Aircraft


class LineFilter(df.FilterSet):
    operator = df.CharFilter(field_name='line__operator__name', lookup_expr='icontains')
    aircraft = df.CharFilter(field_name='line__aircraft__name', lookup_expr='icontains')
    class Meta:
        model = Line
        fields = ('operator', 'aircraft', )


class DepartureFilter(LineFilter):
    city = df.CharFilter(field_name='line__departure_city', lookup_expr='icontains')
    class Meta:
        fields = ('city', )


class ArrivalFilter(LineFilter):
    city = df.CharFilter(field_name='line__arrival_city', lookup_expr='icontains')
    class Meta:
        fields = ('city', )

