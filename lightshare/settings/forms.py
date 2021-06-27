from django.forms import ModelForm
from models import Privacy
from models import User_Feedback

class PrivacyForm(ModelForm):
	
	class Meta:
		model = Privacy
		fields = ['username','email','stats']


class FeedbackForm(ModelForm):
	
	class Meta:
		model = User_Feedback
		fields = ['username','feedback']