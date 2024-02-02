from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Slot, Carrier, Vehicle, Order, Booking, SlotTime, User, Driver


# class CustomUserAdmin(UserAdmin):
#     fieldsets = (
#         *UserAdmin.fieldsets,
#         (
#             'Additional Info',
#             {
#                 'fields': ('carrier',)
#             }
#         )
#     )

# admin.site.register(User, CustomUserAdmin)


fields = list(UserAdmin.fieldsets)
fields[1] = ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'carrier')})
UserAdmin.fieldsets = tuple(fields)

admin.site.register(User, UserAdmin)
admin.site.register(Slot)
admin.site.register(Carrier)
admin.site.register(Vehicle)
admin.site.register(Order)
admin.site.register(Booking)
admin.site.register(SlotTime)
admin.site.register(Driver)
