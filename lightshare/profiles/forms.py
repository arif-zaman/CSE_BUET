from django.forms import ModelForm
from models import Profile

class ProfileForm(ModelForm):

	class Meta:
		model = Profile
		fields = ['firstname','lastname','username','email','propic']