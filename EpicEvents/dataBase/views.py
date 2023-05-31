from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from .models import Event, Contract, Customer, CustomUser
from .serializers import ContractSerializer, CustomerSerializer, EventSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import HasCustomerPermission, HasContractPermission
from .filters import CustomerFilter, ContractFilter, EventFilter
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.db.models import F
class UserRegistrationView(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.create_user(email=request.data['email'],
                                   last_name=request.data['last_name'],
                                   password=request.data['password'],
                                   first_name=request.data['first_name'],
                                   role=request.data['role'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class Customers(ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class  = CustomerFilter
    search_fields = ['first_name', 'last_name', 'email']

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        return queryset

    def list(self, request, *args, **kwargs):

        queryset = self.filter_queryset(self.get_queryset())  # Filtrer le queryset
        serializer = CustomerSerializer(queryset, many=True)  # Utiliser le queryset filtré
        return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)

        if serializer.is_valid():
            if request.user.role != "Sales":
                message = str("Support can't create customers")
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                customer = serializer
                customer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)


class Individual_Customer(ModelViewSet):



    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
    permission_classes = [IsAuthenticated, HasCustomerPermission]


    def retrieve(self, request, *args, **kwargs):
        instance = Customer.objects.get(id=kwargs['id'])
        serializer = CustomerSerializer(instance, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Customer, id=kwargs['id'])
        self.check_object_permissions(self.request, obj)
        instance = Customer.objects.get(id=kwargs['id'])
        serializer = CustomerSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        obj = get_object_or_404(Customer, id=kwargs['id'])
        self.check_object_permissions(self.request, obj)
        self.perform_destroy(obj)
        message = 'Customer deleted'
        return Response({'message': message},
                        status=status.HTTP_204_NO_CONTENT)


class Contracts(ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ContractFilter
    search_fields = ['customer_first_name', 'customer_last_name', 'customer_email']

    def list(self, request, *args, **kwargs):
        instances = self.filter_queryset(self.get_queryset()).annotate(
            customer_first_name=F('customer__first_name'),
            customer_email=F('customer__email')
        )
        serializer = ContractSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = ContractSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['sales_contact'] = request.user
            if request.user.role != "Sales":
                message = str("Support can't create contracts")
                return Response({'message': message}, status=status.HTTP_200_OK)
            else:
                contract = serializer
                contract.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Individual_Contract(ModelViewSet):
    serializer_class = ContractSerializer
    queryset = Contract.objects.all()
    permission_classes = [IsAuthenticated, HasContractPermission]

    def retrieve(self, request, *args, **kwargs):
        instance = Contract.objects.get(id=kwargs['id'])
        serializer = ContractSerializer(instance, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Contract, id=kwargs['id'])
        self.check_object_permissions(self.request, obj)
        instance = Contract.objects.get(id=kwargs['id'])
        serializer = ContractSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        obj = get_object_or_404(Contract, id=kwargs['id'])
        self.check_object_permissions(self.request, obj)
        self.perform_destroy(obj)
        message = 'contract deleted'
        return Response({'message': message},
                        status=status.HTTP_204_NO_CONTENT)


class Events(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = EventFilter
    search_fields = ['contract__customer__first_name', 'contract__customer__last_name', 'contract__customer__email']

    def list(self, request, *args, **kwargs):
        instances = self.filter_queryset(self.get_queryset()).annotate(
            customer_first_name=F('contract__customer__first_name'),
            customer_email=F('contract__customer__email')
        )
        serializer = EventSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.role != "Sales":
                message = str("Support can't create events")
                return Response({'message': message}, status=status.HTTP_200_OK)
            else:
                serializer.save()

                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Individual_Event(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = Event.objects.get(id=kwargs['id'])
        serializer = EventSerializer(instance, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Event, id=kwargs['id'])
        self.check_object_permissions(self.request, obj)
        instance = Event.objects.get(id=kwargs['id'])
        serializer = EventSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        obj = get_object_or_404(Event, id=kwargs['id'])
        self.check_object_permissions(self.request, obj)
        self.perform_destroy(obj)
        message = 'Event deleted'
        return Response({'message': message},
                        status=status.HTTP_204_NO_CONTENT)


