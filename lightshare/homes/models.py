from django.db import models
from django.utils.encoding import smart_unicode

class fav_group(models.Model):
    
    username = models.CharField(max_length =120, db_index=True)
    group_name = models.CharField(max_length =200)
    
    def __unicode__(self):
        
        return smart_unicode(self.username)

    class Meta:
    	ordering = ['username']
    	unique_together = ("username", "group_name")