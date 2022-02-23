from django.contrib import admin
from FuturePlanning.models import MySettings,c_Events,c_Familys,c_Records,UserProfileInfo

# Register your models here.
admin.site.register(c_Familys)
admin.site.register(c_Records)
admin.site.register(c_Events)
admin.site.register(MySettings)
admin.site.register(UserProfileInfo)
