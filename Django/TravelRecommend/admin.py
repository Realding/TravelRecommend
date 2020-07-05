from django.contrib import admin

# Register your models here.
from TravelRecommend import models

admin.site.register(models.UserInfo)
admin.site.register(models.CityInfo)
admin.site.register(models.UserToCity)
admin.site.register(models.IMG)
