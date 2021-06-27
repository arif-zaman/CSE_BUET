from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from models import Profile
from models import Notification
from models import Recent_Activity
from forums.models import Group
from forums.models import GroupArticle
from forums.models import GroupMember
from settings.models import Privacy
from django.contrib.auth.models import User
from forms import ProfileForm


def profile(request,user_id=1):

	if 'name' in request.session:
		name = request.session['name']
		user = Profile.objects.filter(id=user_id)
		name2 = ''
		for u in user:
			name2 = u.username

		if name2==name:
			pro = Profile.objects.get(username=name)

			usr = User.objects.get(username=name)
			num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()
			
			var ={
				'session_name': name,
				'creator': Group.objects.filter(group_creator=name).count(),
				'adm': GroupMember.objects.filter(username=name,status='admin').count(),
				'mod': GroupMember.objects.filter(username=name,status='moderator').count(),
				'usr': GroupMember.objects.filter(username=name).count(),
				'num': num,
				'notifi': Notification.objects.filter(username=name)[:5],
				'post': GroupArticle.objects.filter(writer=name).count(),
				'user': User.objects.get(username=name),
				'pro': pro,
				'ur': pro,
				'ra': Recent_Activity.objects.filter(username=name),
			}
			return render_to_response("profile.html",var,context_instance=RequestContext(request))
		else:
			if len(name2) != 0:

				usr = User.objects.get(username=name)
				num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()
				
				var ={
					'session_name': name,
					'creator': Group.objects.filter(group_creator=name2).count(),
					'adm': GroupMember.objects.filter(username=name2,status='admin').count(),
					'mod': GroupMember.objects.filter(username=name2,status='moderator').count(),
					'usr': GroupMember.objects.filter(username=name2).count(),
					'post': GroupArticle.objects.filter(writer=name2).count(),
					'num': num,
					'notifi': Notification.objects.filter(username=name)[:5],
					'user': User.objects.get(username=name2),
					'pro': Profile.objects.get(username=name2),
					'pri': Privacy.objects.get(username=name2),
					'ur': Profile.objects.get(username=name)
				}
				return render_to_response("profile_view.html",var,context_instance=RequestContext(request))

	return HttpResponseRedirect("/lightshare/login")

def edit_profile(request,user_id=1):

	addr = "/lightshare/user/profile/"+user_id+"/"

	if request.POST:

		name = request.session['name']
		user = Profile.objects.get(username=name)
		user.firstname = request.POST.get("firstname", "")
		user.lastname = request.POST.get("lastname", "")
		user.email = request.POST.get("email", "")
		if request.FILES.get("propic"):
			user.propic = request.FILES.get("propic")
		user.save()

		return HttpResponseRedirect(addr)

	if 'name' in request.session:
		return HttpResponseRedirect(addr)

	return HttpResponseRedirect("/lightshare/login")