from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import get_object_or_404
from .models import Event, Contract, Customer, CustomUser
from .serializers import ContractSerializer, CustomerSerializer, EventSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import HasCustomerPermission, HasEventPermission, HasContractPermission


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
    #authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):

        instances = Customer.objects.all()
        serializer = CustomerSerializer(instances, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            if request.user.role != "Sales":
                message = str("Your role does not allows you to create new customers")
                return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)
            else:
                customer = serializer.save(sales=request.user)
                customer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        obj = get_object_or_404(Customer, id=kwargs['customer_id'])
        self.check_object_permissions(self.request, obj)
        instance = Customer.objects.get(id=kwargs['customer_id'])
        serializer = CustomerSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
