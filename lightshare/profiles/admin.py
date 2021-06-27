from django.contrib import admin

from .models import Profile
from .models import Recent_Activity
from .models import Notification

class ProfileAdmin(admin.ModelAdmin):
    
    list_display = ('username','email')

admin.site.register(Profile,ProfileAdmin)

class RecentAdmin(admin.ModelAdmin):

    list_display = ('username','body')

admin.site.register(Recent_Activity,RecentAdmin)

class NotiAdmin(admin.ModelAdmin):

    list_display = ('username','body')

admin.site.register(Notification,NotiAdmin)