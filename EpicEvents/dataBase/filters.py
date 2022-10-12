import django_filters
from .models import Customer

class CustomerFilter(django_filters.FilterSet):

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email']

'''class ContractFilter(django_filters.FilterSet):
    customer_first_name = django_filters.CharFilter(lookup_expr='icontains')
    customer_last_name = django_filters.CharFilter(lookup_expr='icontains')
    customer_email = django_filters.CharFilter(lookup_expr='icontains')
    date = django_filters.DateFilter(field_name='date', lookup_expr='exact')
    price = django_filters.NumberFilter(field_name='price')
    
    
username = Filter(form_field=forms.CharField(), lookups=['exact'])
    email = Filter(form_field=forms.CharField())
    joined = Filter(form_field=forms.DateField())
    profile = ProfileFilterSet()
'''