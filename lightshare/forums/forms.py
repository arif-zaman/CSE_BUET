from django.forms import ModelForm
from models import Group
from models import GroupArticle
from models import Post_Comment

class ArticleForm(ModelForm):
	
	class Meta:
		model = GroupArticle
		fields = ['title','writer','body','public','group_name']


class GroupForm(ModelForm):
	
	class Meta:
		model = Group
		fields = ['group_name','group_creator','group_category','public','group_description']


class Post_CommentForm(ModelForm):
	
	class Meta:
		model = Post_Comment
		fields = ['comment','commentor','post_id']