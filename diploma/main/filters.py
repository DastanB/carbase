from django_filters import rest_framework as filters
from main.models import Complectation, Offer


class ComplectationFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='contains')
    color = filters.ChoiceFilter(lookup_expr='exact')
    
    min_engine_size = filters.NumberFilter(field_name='engine_size', lookup_expr='gte')
    max_engine_size = filters.NumberFilter(field_name='engine_size', lookup_expr='lte')

    min_power = filters.NumberFilter(field_name='power', lookup_expr='gte')
    max_power = filters.NumberFilter(field_name='power', lookup_expr='lte')

    min_torque = filters.NumberFilter(field_name='torque', lookup_expr='gte')
    max_torque = filters.NumberFilter(field_name='torque', lookup_expr='lte')

    min_year = filters.NumberFilter(field_name='year', lookup_expr='gte')
    max_year = filters.NumberFilter(field_name='year', lookup_expr='lte')

    gearbox = filters.ChoiceFilter(lookup_expr='exact')

    class Meta:
        model = Complectation
        fields = ('name', 'color', 'engine_size', 'power', 'torque', 'drive_train', 'gearbox', 'year',)

class OfferFilter(filters.FilterSet):
    model = filters.CharFilter(field_name='complectation__auto_model__name', lookup_expr='contains')

    min_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Offer
        fields = ('complectation', 'price')