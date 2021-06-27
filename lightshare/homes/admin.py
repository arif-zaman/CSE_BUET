from django.contrib import admin
from .models import fav_group

class Fav_GroupAdmin(admin.ModelAdmin):

	list_display = ('username','group_name')

admin.site.register(fav_group,Fav_GroupAdmin)