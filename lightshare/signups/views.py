from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import auth
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from profiles.models import Profile
from settings.models import Privacy

def signup(request,str=""):
	
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		str1 = request.POST.get("username", "")
		str2 = request.POST.get("email", "")
		user1 = Profile.objects.filter(email=str2)
		user2 = Privacy.objects.filter(email=str2)
		if user1:
			address = '/lightshare/signup/email_alert/'
			return HttpResponseRedirect(address)
			
		else:
			if form.is_valid():
				form.save()
				create_profile(str1,str2)
				create_privacy(str1)
				return HttpResponseRedirect('/lightshare/signup_success')
			else :
				address = '/lightshare/signup/username_alert/'
				return HttpResponseRedirect(address)
		
	args = {}
	args.update(csrf(request))
	args['form'] = UserCreationForm()

	if 'name' in request.session:
		name = request.session['name']
		return HttpResponseRedirect("/lightshare/username")

	alert1 = False
	alert2 = False
	if str == "email_alert":
		alert1=True
	if str == "username_alert":
		alert2=True

	var = {
		'args': args,
		'alert1': alert1,
		'alert2': alert2
	}
	return render_to_response("signup.html",var, context_instance=RequestContext(request))

def signup_success(request):

	return render_to_response("signup_success.html")

def create_profile(str1,str2):
	user = Profile(username=str1,email=str2)
	user.save()

def create_privacy(str1):
	user = Privacy(username=str1)
	user.save()