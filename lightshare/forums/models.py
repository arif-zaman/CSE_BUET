from django.db import models
from django.utils.encoding import smart_unicode

class Group(models.Model):
    
    group_name = models.CharField(max_length =200,unique=True)
    group_creator = models.CharField(max_length =120)
    group_category = models.CharField(max_length =120, db_index=True)
    public = models.BooleanField(default=True)
    group_description = models.CharField(max_length =1500)
    propic = models.FileField(upload_to='Files/%Y/%m/%d',null=True,blank=True)
    isactive = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __unicode__(self):
        
        return smart_unicode(self.group_name)

    class Meta:
        ordering = ['group_category']

class GroupArticle(models.Model):
    
    title = models.CharField(max_length =300)
    writer = models.CharField(max_length =120)
    body = models.TextField()
    public = models.BooleanField(default=False)
    group_name = models.CharField(max_length =200, db_index=True)
    likes = models.IntegerField(default=0)
    pinned = models.BooleanField(default=False)
    isactive = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    modified = models.DateTimeField(auto_now_add=False, auto_now=True)
    
    def __unicode__(self):
        
        return smart_unicode(self.title)

    class Meta:
        ordering = ['-pinned','-created']
        

class Post_Comment(models.Model):
    
    comment = models.CharField(max_length =1200)
    commentor = models.CharField(max_length =120)
    post_id = models.IntegerField(db_index=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __unicode__(self):
        
        return smart_unicode(self.id)

    class Meta:
        ordering = ['post_id']

class Post_Like(models.Model):
    
    username = models.CharField(max_length =120)
    post_id = models.IntegerField(db_index=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    
    def __unicode__(self):
        
        return smart_unicode(self.id)

    class Meta:
        ordering = ['post_id']
        unique_together = ("username", "post_id")

class GroupMember(models.Model):
    
    username = models.CharField(max_length =120)
    group_name = models.CharField(max_length =200,db_index=True)
    status = models.CharField(max_length =120)
    join_date = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_verified = models.BooleanField(default=True)
    
    def __unicode__(self):
        
        return smart_unicode(self.join_date)

    class Meta:
        ordering = ['username']
        unique_together = ("username", "group_name")

class GroupCategory(models.Model):

    group_category = models.CharField(max_length =120, unique=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    propic = models.FileField(upload_to='Files/%Y/%m/%d',null=True,blank=True)
    
    def __unicode__(self):
        
        return smart_unicode(self.group_category)

    class Meta:
        ordering = ['group_category']