from rest_framework import serializers
from .models import Event, Contract, Customer, CustomUser


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create_user(self, email, password, role, first_name=None, last_name=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        user = CustomUser.objects.create(
            email=email,
            role=role
        )
        if first_name and isinstance(first_name, str):
            user.first_name = first_name
        else:
            user.first_name = ""
        if last_name and isinstance(last_name, str):
            user.last_name = last_name
        else:
            user.last_name = ""
        user.set_password(password)
        user.save()
        return user


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            'id', 'sales_contact', 'first_name', 'last_name', 'email',
            'mobile', 'company_name', 'date_created', 'date_updated'
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'date_creation': {'read_only': True},
            'date_update': {'read_only': True},
            'sales': {'read_only': True},
        }


class ContractSerializer(serializers.ModelSerializer):
    customer_first_name = serializers.CharField(source='customer.first_name', read_only=True)
    customer_last_name = serializers.CharField(source='customer.last_name', read_only=True)

    class Meta:
        model = Contract
        fields = ['id', 'customer', 'customer_first_name', 'customer_last_name', 'sales_contact', 'amount', 'payment_due', 'status', 'date_created']
        extra_kwargs = {
            'id': {'read_only': True},
            'sales_contact': {'read_only': True},
            'date_created': {'read_only': True},
        }

class EventSerializer(serializers.ModelSerializer):
    customer_first_name = serializers.CharField(source='contract.customer.first_name', read_only=True)
    customer_last_name = serializers.CharField(source='contract.customer.last_name', read_only=True)

    class Meta:
        model = Event
        fields = ['id', 'contract', 'customer_first_name', 'customer_last_name', 'event_date', 'support_contact', 'event_status','attendees','notes', 'date_created']
        extra_kwargs = {
            'id': {'read_only': True},
            'time_created': {'read_only': True}
        }
