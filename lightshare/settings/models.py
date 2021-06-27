from django.db import models
from django.utils.encoding import smart_unicode

class Privacy(models.Model):
    
    username = models.CharField(max_length =120,unique=True)
    email = models.BooleanField(default=True)
    stats = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now_add=True, auto_now=True)
    
    def __unicode__(self):
        
        return smart_unicode(self.username)

class User_Feedback(models.Model):
    
    username = models.CharField(max_length =120)
    feedback = models.TextField(max_length =1000)
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        
        return smart_unicode(self.username)

    class Meta:
        ordering = ['-created']
        unique_together = ("username","feedback")