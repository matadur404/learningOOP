from django.contrib import admin
from .models import *


admin.site.register(Manufacturer)
admin.site.register(PlaneModel)
admin.site.register(Aircraft)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Airport)
admin.site.register(Operator)
admin.site.register(Line)
admin.site.register(Flight)