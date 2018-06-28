from django.contrib import admin
from .models import Holders, Buy, Sell, Shares, Profile, Plan, History, Raise, Favoriten

admin.site.register(Holders)
admin.site.register(Buy)
admin.site.register(Sell)
admin.site.register(Shares)
admin.site.register(Profile)
admin.site.register(Plan)
admin.site.register(History)
admin.site.register(Raise)
admin.site.register(Favoriten)


# Register your models here.
