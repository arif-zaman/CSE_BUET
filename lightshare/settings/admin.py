from django.contrib import admin
from .models import Privacy
from .models import User_Feedback

class PrivacyAdmin(admin.ModelAdmin):

    list_display = ('username','email','stats')

admin.site.register(Privacy,PrivacyAdmin)

class User_FeedbackAdmin(admin.ModelAdmin):

	list_display = ('username','feedback')

admin.site.register(User_Feedback,User_FeedbackAdmin)