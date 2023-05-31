import django_filters
from .models import Customer, Contract, Event

class CustomerFilter(django_filters.FilterSet):

    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email']

class ContractFilter(django_filters.FilterSet):
    customer_first_name = django_filters.CharFilter(field_name='customer__first_name', lookup_expr='icontains')
    customer_last_name = django_filters.CharFilter(field_name='customer__last_name', lookup_expr='icontains')
    customer_email = django_filters.CharFilter(field_name='customer__email', lookup_expr='icontains')

    class Meta:
        model = Contract
        fields = ['customer_first_name', 'customer_last_name', 'customer_email']


import django_filters
from .models import Event

class EventFilter(django_filters.FilterSet):
    customer_first_name = django_filters.CharFilter(field_name='contract__customer__first_name', lookup_expr='icontains')
    customer_last_name = django_filters.CharFilter(field_name='contract__customer__last_name', lookup_expr='icontains')
    customer_email = django_filters.CharFilter(field_name='contract__customer__email', lookup_expr='icontains')

    class Meta:
        model = Event
        fields = ['customer_first_name', 'customer_last_name', 'customer_email']