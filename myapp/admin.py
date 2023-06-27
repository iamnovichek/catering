from django.contrib import admin
from .models import Order, Menu, History


admin.site.register(History)
admin.site.register(Menu)
admin.site.register(Order)
