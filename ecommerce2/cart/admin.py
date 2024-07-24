from django.contrib import admin
from .models import Cart,Order_details,Payment
# Register your models here.
admin.site.register(Cart)
admin.site.register(Order_details)
admin.site.register(Payment)