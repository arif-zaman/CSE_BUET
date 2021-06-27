from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from models import fav_group
from forums.models import Group
from profiles.models import Profile
from forums.models import GroupMember
from profiles.models import Notification
from django.contrib.auth.models import User
from django.core.context_processors import csrf


def get_fav(str1):
	list1 = []
	list2 = []
	favs = fav_group.objects.filter(username=str1)
	group = Group.objects.all()
	for j in group:
		for i in favs:
			if i.group_name == j.group_name:
				list1.append(j.id)
				list2.append(j.group_name)

	fav_list = dict(zip(list1, list2))
	return fav_list


def get_adm(str1, str2, test):
	list1 = []
	list2 = []

	if test == 1:
		adm = GroupMember.objects.filter(username=str1).exclude(status=str2)
	else:
		adm = GroupMember.objects.filter(username=str1).exclude(status=str2)[:3]

	group = Group.objects.all()

	for j in group:
		for i in adm:
			if i.group_name == j.group_name:
				list1.append(j.id)
				list2.append(j.group_name)

	adm_list = dict(zip(list1, list2))
	return adm_list


def get_all(str1, test):
	list1 = []
	list2 = []

	if test == 1:
		adm = GroupMember.objects.filter(username=str1)
	else:
		adm = GroupMember.objects.filter(username=str1)[:3]

	group = Group.objects.all()

	for j in group:
		for i in adm:
			if i.group_name == j.group_name:
				list1.append(j.id)
				list2.append(j.group_name)

	adm_list = dict(zip(list1, list2))
	return adm_list


def get_rec(str1, test):
	list1 = []
	list2 = []

	if test == 1:
		adm = GroupMember.objects.exclude(username=str1)
	else:
		adm = GroupMember.objects.exclude(username=str1)[:3]

	group = Group.objects.all()

	for j in group:
		for i in adm:
			if i.group_name == j.group_name:
				list1.append(j.id)
				list2.append(j.group_name)

	adm_list = dict(zip(list1, list2))
	return adm_list


def home(request):
	if 'name' in request.session:
		name = request.session['name']
		return HttpResponseRedirect("/lightshare/userhome/")

	return render_to_response("home_logout.html")


def mhome(request):
	if 'name' in request.session:
		name = request.session['name']
		name1 = 'user'
		usr = User.objects.get(username=name)
		num = Notification.objects.filter(username=name, timestamp__gt=usr.last_login).count()

		var = {
			'session_name': name,
			'favs_list': get_fav(name),
			'ad': get_adm(name, name1, 0),
			'num': num,
			'notifi': Notification.objects.filter(username=name)[:5],
			'all': get_all(name, 0),
			'rec': get_rec(name, 0),
			'ur': Profile.objects.get(username=name)
		}
		return render_to_response("home_login.html", var, context_instance=RequestContext(request))

	return HttpResponseRedirect("/lightshare/login")


def noti(request):
	if 'name' in request.session:
		name = request.session['name']
		name1 = 'user'
		usr = User.objects.get(username=name)
		num = Notification.objects.filter(username=name, timestamp__gt=usr.last_login).count()

		var = {
			'session_name': name,
			'favs_list': get_fav(name),
			'num': num,
			'notifi': Notification.objects.filter(username=name)[:5],
			'noti': Notification.objects.filter(username=name)[:200],
			'ur': Profile.objects.get(username=name)
		}
		return render_to_response("notifications.html", var, context_instance=RequestContext(request))

	return HttpResponseRedirect("/lightshare/login")


def admod(request):
	if 'name' in request.session:
		name = request.session['name']
		name1 = 'user'
		usr = User.objects.get(username=name)
		num = Notification.objects.filter(username=name, timestamp__gt=usr.last_login).count()

		var = {
			'session_name': name,
			'favs_list': get_fav(name),
			'num': num,
			'notifi': Notification.objects.filter(username=name)[:5],
			'ad': get_adm(name, name1, 1),
			'ur': Profile.objects.get(username=name)
		}
		return render_to_response("group_list_admin_moderator.html", var, context_instance=RequestContext(request))

	return HttpResponseRedirect("/lightshare/login")


def all(request):
	if 'name' in request.session:
		name = request.session['name']
		usr = User.objects.get(username=name)
		num = Notification.objects.filter(username=name, timestamp__gt=usr.last_login).count()

		var = {
			'session_name': name,
			'favs_list': get_fav(name),
			'num': num,
			'notifi': Notification.objects.filter(username=name)[:5],
			'ur': Profile.objects.get(username=name),
			'all': get_all(name, 1)
		}
		return render_to_response("group_list_all.html", var, context_instance=RequestContext(request))

	return HttpResponseRedirect("/lightshare/login")


def recommended(request):
	if 'name' in request.session:
		name = request.session['name']
		usr = User.objects.get(username=name)
		num = Notification.objects.filter(username=name, timestamp__gt=usr.last_login).count()

		var = {
			'session_name': name,
			'favs_list': get_fav(name),
			'num': num,
			'notifi': Notification.objects.filter(username=name)[:5],
			'ur': Profile.objects.get(username=name),
			'rec': get_rec(name, 1)
		}
		return render_to_response("group_list_recommended.html", var, context_instance=RequestContext(request))

	return HttpResponseRedirect("/lightshare/login")


def search(request, page_id=1, str=""):
	if 'name' in request.session:
		name = request.session['name']
		str1 = ""

		if str == "$":

			if request.method == 'POST':
				str1 = request.POST.get("search", "")
		else:

			str1 = str

		usr = User.objects.get(username=name)
		num = Notification.objects.filter(username=name, timestamp__gt=usr.last_login).count()

		if len(str1) == 0:

			invalid = True
			count = 0

			var = {
				'session_name': name,
				'favs_list': get_fav(name),
				'invalid': invalid,
				'num': num,
				'notifi': Notification.objects.filter(username=name)[:5],
				'count': count,
				'ur': Profile.objects.get(username=name)
			}

		else:

			invalid = False
			count = Group.objects.filter(group_name__icontains=str1).count()
			pid1 = int(page_id)
			num = pid1 * 5
			s1 = num - 5

			if count > 5 and pid1 != 1:
				new = True
			else:
				new = False

			if count > num:
				old = True
			else:
				old = False

			var = {
				'session_name': name,
				'favs_list': get_fav(name),
				'invalid': invalid,
				'new': new,
				'old': old,
				'count': count,
				'pid': page_id,
				'num': num,
				'notifi': Notification.objects.filter(username=name)[:5],
				'str1': str1,
				'group': Group.objects.filter(group_name__icontains=str1)[s1:num],
				'ur': Profile.objects.get(username=name)
			}

		return render_to_response("search_result.html", var, context_instance=RequestContext(request))

	return HttpResponseRedirect("/lightshare/login/")


def custom404(request):
	return render_to_response("custom_404.html")


def custom500(request):
	return render_to_response("custom_500.html")