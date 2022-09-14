from django.urls import path, include, re_path
import django.contrib.auth.urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, Customers

urlpatterns = [
    path('add_user/', UserRegistrationView.as_view({'post': 'create'})),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),

    re_path('customers/$', Customers.as_view({'get': 'list', 'post': 'create', 'put': 'update'})),
]
'''
path customers
path customers/id
path contracts
path contracts/id
path events
path events/id
'''
