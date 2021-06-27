from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from profiles.models import Profile
from forms import PrivacyForm
from forms import FeedbackForm
from models import Privacy
from models import User_Feedback
from homes.models import fav_group
from profiles.models import Notification
from profiles.models import Recent_Activity
from django.contrib.auth.models import User
from django.core.context_processors import csrf

def report(request):

	if request.POST:
		form =FeedbackForm(request.POST)
		if form.is_valid():
			form.save()
			address = '/lightshare/userhome/'
			return HttpResponseRedirect(address)

	args = {}
	args.update(csrf(request))
	args['form'] = FeedbackForm()

	if 'name' in request.session:
		name = request.session['name']

		usr = User.objects.get(username=name)
		num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()

		var = {
			'session_name': name,
			'args': args,
			'num': num,
			'notifi': Notification.objects.filter(username=name)[:5],
			'ur': Profile.objects.get(username=name)
		}
		return render_to_response("report_problem.html",var, context_instance=RequestContext(request))

	return HttpResponseRedirect("/lightshare/login")

def privacy(request):

	if request.POST:
		name = request.session['name']
		user = Privacy.objects.get(username=name)
		user.email = request.POST.get("email","")
		user.stats = request.POST.get("stats","")
		user.save()
		address = '/lightshare/userhome/'
		return HttpResponseRedirect(address)

	if 'name' in request.session:
		name = request.session['name']

		usr = User.objects.get(username=name)
		num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()
		
		var = {
			'session_name': name,
			'num': num,
			'notifi': Notification.objects.filter(username=name)[:5],
			'ur': Profile.objects.get(username=name),
			'pri': Privacy.objects.get(username=name)
		}
		return render_to_response("privacy_setting.html",var, context_instance=RequestContext(request))

	return HttpResponseRedirect("/lightshare/login")

def chpass(request,str=""):

	if request.POST:
		name = request.session['name']
		password1 = request.POST.get("password1","")
		password2 = request.POST.get("password2","")
		user = User.objects.get(username=name)

		if user.check_password(password1):
			user.set_password(password2)
			user.save()
			address = '/lightshare/change_password/success/'
			return HttpResponseRedirect(address)
		else :
			address = '/lightshare/change_password/warning/'
			return HttpResponseRedirect(address)

	if 'name' in request.session:
		name = request.session['name']
		alert = False
		success = False
		if str == "warning":
			alert=True
		if str == "success":
			success=True

		usr = User.objects.get(username=name)
		num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()
		
		var = {
			'session_name': name,
			'num': num,
			'notifi': Notification.objects.filter(username=name)[:5],
			'ur': Profile.objects.get(username=name),
			'alert': alert,
			'success': success
		}
		return render_to_response("change_password.html",var, context_instance=RequestContext(request))

def deactive(request,str=""):

	if request.POST:
		name = request.session['name']
		password1 = request.POST.get("password1","")
		user = User.objects.get(username=name)

		if user.check_password(password1):
			user.delete()
			usr = Profile.objects.get(username=name)
			usr.delete()
			fav = fav_group.objects.filter(username=name)
			if fav:
				fav.delete()
			pri = Privacy.objects.get(username=name)
			pri.delete()
			ra = Recent_Activity.objects.filter(username=name)
			if ra:
				ra.delete()
			noti = Notification.objects.filter(username=name)
			if noti:
				noti.delete()

			address = '/lightshare/logout/'
			return HttpResponseRedirect(address)
		else :
			address = '/lightshare/deactivate/warning/'
			return HttpResponseRedirect(address)

	if 'name' in request.session:
		name = request.session['name']
		alert = False

		if str == "warning":
			alert=True

		usr = User.objects.get(username=name)
		num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()
		
		var = {
			'session_name': name,
			'num': num,
			'notifi': Notification.objects.filter(username=name)[:5],
			'ur': Profile.objects.get(username=name),
			'alert': alert
		}
		return render_to_response("deactive.html",var, context_instance=RequestContext(request))