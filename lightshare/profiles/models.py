from django.db import models
from django.utils.encoding import smart_unicode

class Profile(models.Model):
    
    firstname = models.CharField(max_length =120,null=True,blank=True)
    lastname = models.CharField(max_length =120,null=True,blank=True)
    username = models.CharField(max_length =120,unique=True)
    email = models.EmailField(unique=True)
    propic = models.FileField(upload_to='Files/%Y/%m/%d',null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __unicode__(self):
        
        return smart_unicode(self.username)

    class Meta:
        ordering = ['username']

class Recent_Activity(models.Model):
    
    username = models.CharField(max_length =120,db_index=True)
    body = models.TextField(max_length =120)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __unicode__(self):
        
        return smart_unicode(self.username)

    class Meta:
        ordering = ['-timestamp']

class Notification(models.Model):
    
    username = models.CharField(max_length =120,db_index=True)
    body = models.TextField(max_length =120)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __unicode__(self):
        
        return smart_unicode(self.username)

    class Meta:
        ordering = ['-timestamp']