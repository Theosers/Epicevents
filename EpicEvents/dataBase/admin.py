from django.contrib import admin
from .models import CustomUser, Contract, Event, Customer


admin.site.register(CustomUser)
admin.site.register(Contract)
admin.site.register(Event)
admin.site.register(Customer)