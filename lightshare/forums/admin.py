from django.contrib import admin
from .models import Group
from .models import GroupArticle
from .models import Post_Comment
from .models import GroupMember
from .models import GroupCategory
from .models import Post_Like

class GroupAdmin(admin.ModelAdmin):

    list_display = ('id','group_name','group_creator','group_category','isactive')

admin.site.register(Group,GroupAdmin)

class GroupArticleAdmin(admin.ModelAdmin):

	list_display = ('title','writer','created','isactive')

admin.site.register(GroupArticle,GroupArticleAdmin)

class Post_CommentAdmin(admin.ModelAdmin):

    list_display = ('comment','commentor','post_id')

admin.site.register(Post_Comment,Post_CommentAdmin)

class Post_LikeAdmin(admin.ModelAdmin):

    list_display = ('username','post_id')

admin.site.register(Post_Like,Post_LikeAdmin)

class GroupMemberAdmin(admin.ModelAdmin):
    
    list_display = ('username','group_name','status')

admin.site.register(GroupMember,GroupMemberAdmin)

class GroupCategoryAdmin(admin.ModelAdmin):
    
    list_display = ('id','group_category')

admin.site.register(GroupCategory,GroupCategoryAdmin)  