from django.urls import path, include, re_path
import django.contrib.auth.urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegistrationView, Customers, Individual_Customer, Contracts, Individual_Contract, Events, Individual_Event

urlpatterns = [
    path('add_user/', UserRegistrationView.as_view({'post': 'create'})),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='refresh'),

    path('customers/', Customers.as_view({'get': 'list', 'post': 'create'})),
    re_path('customers/(?P<id>[0-9])/$', Individual_Customer.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),
    path('contracts/', Contracts.as_view({'get': 'list', 'post': 'create'})),
    re_path('contracts/(?P<id>[0-9])/$', Individual_Contract.as_view({'get': 'retrieve', 'put':'update', 'delete': 'destroy'})),
    path('events/', Events.as_view({'get': 'list', 'post': 'create'}), name='events_list'),
    re_path('events/(?P<id>[0-9])/$', Individual_Event.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),


    #path('customers/(?P<id>[0-9])/$', Individual_Customer.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})),

]

'''

urlpatterns = [
   
   
    re_path('events/$', Events.as_view({'get': 'list', 'post': 'create'}), name='events_list'),
    re_path('events/(?P<event_id>[0-9])/$', SoloEvent.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}))
]



'''
