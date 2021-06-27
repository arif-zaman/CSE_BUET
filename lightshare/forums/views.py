from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from forms import ArticleForm
from forms import GroupForm
from forms import Post_CommentForm
from models import Group
from models import GroupArticle
from models import Post_Comment
from models import GroupCategory
from models import GroupMember
from models import Post_Like
from homes.models import fav_group
from profiles.models import Profile
from profiles.models import Notification
from profiles.models import Recent_Activity
from django.contrib.auth.models import User
from django.core.context_processors import csrf

def get_fav(str1):

	list1 = []
	list2 = []
	favs = fav_group.objects.filter(username=str1)
	group = Group.objects.all()
	for j in group :
		for i in favs:
			if i.group_name==j.group_name:
				list1.append(j.id)
				list2.append(j.group_name)

	fav_list = dict(zip(list1,list2))
	return fav_list

def scategory(request):

	if 'name' in request.session:
		name = request.session['name']
		usr = User.objects.get(username=name)
		num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()

		var = {
			'session_name': name,
			'favs_list': get_fav(name),
			'ur': Profile.objects.get(username=name),
			'num': num,
			'notifi': Notification.objects.filter(username=name)[:5],
			'categories': GroupCategory.objects.all()
		}
		return render_to_response("select_category.html",var, context_instance=RequestContext(request))

	return HttpResponseRedirect("/lightshare/login")

def cgroup(request,cat_id=1):

	if request.POST:
		form = GroupForm(request.POST)
		if form.is_valid():
			form.save()
			name2 = request.POST.get("group_name", "")
			gg = Group.objects.get(group_name=name2)
			gid = str(gg.id)
			name = request.POST.get("group_creator", "")
			addr = '/lightshare/'+gid+'/home/'
			str1 = "You have created a group named <a href='"+addr+"'>"+name2+"</a>" 
			recentactivity(name,str1)
			address = '/lightshare/'+gid+'/jgroup/1/'
			return HttpResponseRedirect(address)
		
	args = {}
	args.update(csrf(request))
	args['form'] = GroupForm()

	if 'name' in request.session:
		name = request.session['name']
		usr = User.objects.get(username=name)
		num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()
		
		var = {
			'session_name': name,
			'favs_list': get_fav(name),
			'num': num,
			'notifi': Notification.objects.filter(username=name)[:5],
			'cat': GroupCategory.objects.get(id=cat_id),
			'ur': Profile.objects.get(username=name),
			'args': args
		}
		return render_to_response("creategroup.html",var, context_instance=RequestContext(request))

	return HttpResponseRedirect("/lightshare/login")


def ghome(request,group_id=1):

	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = get_group_name.group_name
		b = GroupMember.objects.filter(username=name,group_name=name2,is_verified=True)

		if get_group_name.isactive:

			count = GroupArticle.objects.filter(group_name=name2,isactive=True).count()
			page_id = 1
			new = False

			if count>5:
				old = True
			else:
				old = False

			chk = 'user'
			ad = GroupMember.objects.filter(username=name,group_name=name2).exclude(status=chk)

			if ad:
				ap = True
			else:
				ap = False

			if b:

				usr = User.objects.get(username=name)
				num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()

				var = {
					'session_name': name,
					'favs_list': get_fav(name),
					'gname': get_group_name,
					'new': new,
					'old': old,
					'num': num,
					'notifi': Notification.objects.filter(username=name)[:5],
					'pid': page_id,
					'adm': ap,
					'fav': fav_group.objects.filter(username=name,group_name=name2),
					'ur': Profile.objects.get(username=name),
					'articles': GroupArticle.objects.filter(group_name=name2,isactive=True)[:5]
				}
				return render_to_response("group_home.html",var, context_instance=RequestContext(request))
			else :
				address='/lightshare/'+group_id+'/profile/'
				return HttpResponseRedirect(address)
		else :
			return HttpResponseRedirect("/lightshare/userhome/")

	return HttpResponseRedirect("/lightshare/login")

def gpage(request,group_id=1,page_id=1):

	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = get_group_name.group_name
		b = GroupMember.objects.filter(username=name,group_name=name2,is_verified=True)

		if get_group_name.isactive:
			count = GroupArticle.objects.filter(group_name=name2,isactive=True).count()
			pid1 = int(page_id)
			num = pid1*5
			s1=num-5

			if count>5:
				new = True
			else:
				new = False

			if count>num:
				old = True
			else:
				old = False

			chk = 'user'
			ad = GroupMember.objects.filter(username=name,group_name=name2).exclude(status=chk)

			if ad:
				ap = True
			else:
				ap = False

			if b:
				usr = User.objects.get(username=name)
				num2 = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()

				var = {
					'session_name': name,
					'favs_list': get_fav(name),
					'gname': get_group_name,
					'new': new,
					'old': old,
					'num': num2,
					'notifi': Notification.objects.filter(username=name)[:5],
					'pid': page_id,
					'adm': ap,
					'fav': fav_group.objects.filter(username=name,group_name=name2),
					'ur': Profile.objects.get(username=name),
					'count': count,
					'articles': GroupArticle.objects.filter(group_name=name2,isactive=True)[s1:num]
				}
				return render_to_response("group_home.html",var, context_instance=RequestContext(request))
			else :
				address='/lightshare/'+group_id+'/profile/'
				return HttpResponseRedirect(address)
		else :
			return HttpResponseRedirect("/lightshare/userhome/")

	return HttpResponseRedirect("/lightshare/login")

def cpost(request,group_id=1):

	if request.POST:
		form = ArticleForm(request.POST)
		if form.is_valid():
			form.save()
			title = request.POST.get("title", "")
			name = request.POST.get("writer", "")
			body = request.POST.get("body", "")
			name2 = request.POST.get("group_name", "")
			gg = GroupArticle.objects.get(title=title,writer=name,body=body,group_name=name2,isactive=True)
			post_id = str(gg.id)
			wtr = gg.writer
			addr = '/lightshare/'+group_id+'/'+post_id+'/'
			str1 = "You write a <a href='"+addr+"'>post</a> at "+name2+"" 
			recentactivity(name,str1)
			noti = GroupMember.objects.filter(group_name=name2,is_verified=True)
			for n in noti:
				if name!=n.username:
					str3 = "<a href='"+addr+"'>"+wtr+" posted on "+name2+"</a>"
					notifications(n.username,str3)

			address = '/lightshare/'+group_id+'/home'
			return HttpResponseRedirect(address)
		
	args = {}
	args.update(csrf(request))
	args['form'] = ArticleForm()

	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = get_group_name.group_name
		b = GroupMember.objects.filter(username=name,group_name=name2,is_verified=True)

		if get_group_name.isactive:
			chk = 'user'
			ad = GroupMember.objects.filter(username=name,group_name=name2).exclude(status=chk)

			if ad:
				ap = True
			else:
				ap = False
			np = True

			if b:

				usr = User.objects.get(username=name)
				num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()

				var ={
					'session_name': name,
					'favs_list': get_fav(name),
					'fav': fav_group.objects.filter(username=name,group_name=name2),
					'gname': get_group_name,
					'adm': ap,
					'num': num,
					'notifi': Notification.objects.filter(username=name)[:5],
					'ur': Profile.objects.get(username=name),
					'args': args
				}
				return render_to_response( "create_post.html", var, context_instance=RequestContext(request))

			else :
				address='/lightshare/'+group_id+'/profile/'
				return HttpResponseRedirect(address)
		else :
			return HttpResponseRedirect("/lightshare/userhome/")

	return HttpResponseRedirect("/lightshare/login")

def gpost(request,group_id =1,post_id=1):

	if request.POST:
		form = Post_CommentForm(request.POST)
		if form.is_valid():
			form.save()
			name = request.session['name']
			try:
				get_group_name = Group.objects.get(id=group_id)
			except:
				return HttpResponseRedirect('/lightshare/userhome/')

			name2 = get_group_name.group_name
			address = '/lightshare/'+group_id+'/'+post_id+'/'
			str1 = "You commented on a <a href='"+address+"'>post</a> of "+name2+"" 
			recentactivity(name,str1)
			noti = GroupArticle.objects.get(id=post_id,isactive=True)
			wtr = noti.writer
			if name!=wtr:
				str3 = "<a href='"+address+"'>"+name+" comments on your post on "+name2+"</a>"
				notifications(wtr,str3)
			return HttpResponseRedirect(address)
		
	args = {}
	args.update(csrf(request))
	args['form'] = Post_CommentForm()

	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')
			
		name2 = get_group_name.group_name
		b = GroupMember.objects.filter(username=name,group_name=name2,is_verified=True)

		if get_group_name.isactive:
			article = GroupArticle.objects.get(id=post_id)
			wtr = article.writer
			su = False
			if name==wtr:
				su = True

			chk = 'user'
			ad = GroupMember.objects.filter(username=name,group_name=name2).exclude(status=chk)

			if ad:
				ap = True
			else:
				ap = False

			if b:

				usr = User.objects.get(username=name)
				num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()
				
				var ={
					'session_name': name,
					'favs_list': get_fav(name),
					'fav': fav_group.objects.filter(username=name,group_name=name2),
					'gname': Group.objects.get(id=group_id),
					'article': article,
					'num': num,
					'notifi': Notification.objects.filter(username=name)[:5],
					'comment': Post_Comment.objects.filter(post_id=post_id),
					'cc': Post_Comment.objects.filter(post_id=post_id).count(),
					'like': Post_Like.objects.filter( username=name,post_id=post_id),
					'ur': Profile.objects.get(username=name),
					'usr': Profile.objects.get(username=wtr),
					'adm': ap,
					'su': su,
					'pid': post_id
				}
				return render_to_response("group_post.html",var, context_instance=RequestContext(request))

			else:

				usr = User.objects.get(username=name)
				num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()

				a = GroupArticle.objects.filter(id=post_id,public=True,isactive=True)

				np = True
				if a:
					var ={
						'session_name': name,
						'favs_list': get_fav(name),
						'gname': Group.objects.get(id=group_id),
						'article': GroupArticle.objects.get(id=post_id,isactive=True),
						'num': num,
						'notifi': Notification.objects.filter(username=name)[:5],
						'comment': Post_Comment.objects.filter(post_id=post_id),
						'cc': Post_Comment.objects.filter(post_id=post_id).count(),
						'like': Post_Like.objects.filter( username=name,post_id=post_id),
						'ur': Profile.objects.get(username=name),
						'np': np, 
						'pid': post_id
					}
					return render_to_response("group_post.html",var, context_instance=RequestContext(request))

				else:
					address='/lightshare/'+group_id+'/profile/'
					return HttpResponseRedirect(address)
		else :
			return HttpResponseRedirect("/lightshare/userhome/")

	return HttpResponseRedirect("/lightshare/login")

def plike(request,group_id=1,post_id=1):
	
	if 'name' in request.session:
		name = request.session['name']
		a = GroupArticle.objects.get(id=post_id,isactive=True)
		b = likedb(name,post_id)
		address = "/lightshare/"+group_id+"/"+post_id+"/"

		if b==1:
			count = a.likes
			count = count+1
			a.likes = count
			gname = a.group_name
			a.save()
			str1 = "You likes a <a href='"+address+"'>post</a> of "+gname+" group "
			recentactivity(name,str1)
			noti = GroupArticle.objects.get(id=post_id,isactive=True)
			wtr = noti.writer
			str3 = "<a href='"+address+"'>"+name+" likes your post on "+gname+"</a>"
			notifications(wtr,str3)

		return HttpResponseRedirect(address)

	return HttpResponseRedirect("/lightshare/login")

def ulike(request,group_id=1,post_id=1):
	
	if 'name' in request.session:
		name = request.session['name']
		a = GroupArticle.objects.get(id=post_id,isactive=True)
		b = unlikedb(name,post_id)
		address = "/lightshare/"+group_id+"/"+post_id+"/"
		
		if b==1:
			count = a.likes
			count = count-1
			a.likes = count
			gname = a.group_name
			a.save()
			str1 = "You unlikes a <a href='"+address+"'>post</a> of "+gname+" group "
			recentactivity(name,str1)

		return HttpResponseRedirect(address)

	return HttpResponseRedirect("/lightshare/login")

def likedb(str1,str2):
	
	b = Post_Like(username=str1,post_id=str2)
	b.save()	
	return 1

def unlikedb(str1,str2):
	
	b = Post_Like.objects.get(username=str1,post_id=str2)

	if b:
		b.delete()
		return 1
	else:
		return 0

def recentactivity(str1,str2):
	
	b = Recent_Activity(username=str1,body=str2)
	b.save()

def notifications(str1,str2):
	
	b = Notification(username=str1,body=str2)
	b.save()

def gprofile(request,group_id =1):

	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome')
		

		if get_group_name.isactive:
			name2 = get_group_name.group_name
			des = get_group_name.group_description
			gm = GroupMember.objects.filter(username=name,group_name=name2)

			if gm:
				np=False
			else:
				np=True

			chk = 'user'
			ad = GroupMember.objects.filter(username=name,group_name=name2).exclude(status=chk)

			if ad:
				ap = True
			else:
				ap = False

			usr = User.objects.get(username=name)
			num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()

			var ={
				'session_name': name,
				'favs_list': get_fav(name),
				'gname': get_group_name,
				'gd': des,
				'num': num,
				'notifi': Notification.objects.filter(username=name)[:5],
				'fav': fav_group.objects.filter(username=name,group_name=name2),
				'gm': gm,
				'np': np,
				'adm': ap,
				'ur': Profile.objects.get(username=name),
				'articles': GroupArticle.objects.filter(group_name=name2,public=True,isactive=True)[:5]
			}
			return render_to_response("group_profile.html",var, context_instance=RequestContext(request))

		else :
			return HttpResponseRedirect("/lightshare/userhome/")

	return HttpResponseRedirect("/lightshare/login")

def member(request,group_id=1):
	
	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')
		
		if get_group_name.isactive:
			name2 = get_group_name.group_name
			b = GroupMember.objects.filter(username=name,group_name=name2,is_verified=True)
			chk = 'user'
			ad = GroupMember.objects.filter(username=name,group_name=name2).exclude(status=chk)

			if ad:
				ap = True
			else:
				ap = False

			if b:

				usr = User.objects.get(username=name)
				num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()
				
				var ={
					'session_name': name,
					'favs_list': get_fav(name),
					'gname': get_group_name,
					'fav': fav_group.objects.filter(username=name,group_name=name2),
					'ur': Profile.objects.get(username=name),
					'num': num,
					'notifi': Notification.objects.filter(username=name)[:5],
					'adm':ap,
					'gmember': GroupMember.objects.filter(group_name=name2,is_verified=True)
				}
				return render_to_response("group_member.html",var, context_instance=RequestContext(request))

			else :
				address='/lightshare/'+group_id+'/profile/'
				return HttpResponseRedirect(address)

		else :
			return HttpResponseRedirect("/lightshare/userhome/")

	return HttpResponseRedirect("/lightshare/login")

def add_fav(request,group_id=1):
	
	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = get_group_name.group_name
		b = fav_group(username=name,group_name=name2)
		b.save()
		address = '/lightshare/'+group_id+'/home/'
		str1 = "You added  <a href='"+address+"'>"+name2+"</a> to your favourite group list" 
		recentactivity(name,str1)
		return HttpResponseRedirect(address)

	return HttpResponseRedirect("/lightshare/login")

def rem_fav(request,group_id=1):
	
	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = get_group_name.group_name
		b = fav_group.objects.filter(username=name,group_name=name2)
		address = '/lightshare/'+group_id+'/home/'

		if b:
			b.delete()
			str1 = "You removed <a href='"+address+"'>"+name2+"</a> from your favourite group list" 
			recentactivity(name,str1)

		return HttpResponseRedirect(address)

	return HttpResponseRedirect("/lightshare/login")

def jgroup(request,group_id=1,status=3):
	
	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = get_group_name.group_name
		list3 = ['admin','admin','moderator','user']
		n=int(status)
		name3 = list3[n]

		address = '/lightshare/'+group_id+'/home/'
		str1 = "You have joined <a href='"+address+"'>"+name2+"</a>"

		if n==1:
			b = GroupMember(username=name,group_name=name2,status=name3)
			recentactivity(name,str1)
		elif get_group_name.public:
			b = GroupMember(username=name,group_name=name2,status=name3)
			recentactivity(name,str1)
		else:
			b = GroupMember(username=name,group_name=name2,status=name3,is_verified=False)
			str1 = "You have asked to join <a href='"+address+"'>"+name2+"</a>"
			recentactivity(name,str1)

		b.save()
		
		
		return HttpResponseRedirect(address)

	return HttpResponseRedirect("/lightshare/login")

def accept(request,group_id=1,str=""):

	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = get_group_name.group_name
		address = '/lightshare/'+group_id+'/dashboard/'
		usr = GroupMember.objects.filter(username=str,group_name=name2)

		if usr:
			user = GroupMember.objects.get(username=str,group_name=name2)
			user.is_verified = True
			user.save()
			addr = '/lightshare/'+group_id+'/home/'
			str1 = "You accepted "+str+" request to join <a href='"+addr+"'>"+name2+"</a>"
			recentactivity(name,str1)
			str2 ="<a href='"+addr+"'>"+name+" accept your request to join group "+name2+"</a>"
			notifications(str,str2)

			return HttpResponseRedirect(address)

	return HttpResponseRedirect("/lightshare/login")

def ignore(request,group_id=1,str=""):

	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = get_group_name.group_name
		address = '/lightshare/'+group_id+'/dashboard/'
		usr = GroupMember.objects.filter(username=str,group_name=name2)

		if usr:
			user = GroupMember.objects.get(username=str,group_name=name2)
			user.delete()
			addr = '/lightshare/'+group_id+'/home/'
			str1 = "You ignored "+str+" request to join <a href='"+addr+"'>"+name2+"</a>"
			recentactivity(name,str1)
			str2 ="<a href='"+addr+"'>Your request to join group "+name2+" has been ignored</a>"
			notifications(str,str2)

			return HttpResponseRedirect(address)

	return HttpResponseRedirect("/lightshare/login")

def lgroup(request,group_id=1):
	
	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = get_group_name.group_name
		b = GroupMember.objects.filter(username=name,group_name=name2)
		add = '/lightshare/'+group_id+'/home/'
		if b:
			b.delete()
			str1 = "You leaved <a href='"+add+"'>"+name2+"</a>" 
			recentactivity(name,str1)
		address = '/lightshare/'+group_id+'/rem_fav/'
		return HttpResponseRedirect(address)

	return HttpResponseRedirect("/lightshare/login")

def search(request,group_id=1,page_id=1,str=""):

	if 'name' in request.session:
		name = request.session['name']
		str1 = ""
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		if get_group_name.isactive:
			name2 = get_group_name.group_name
			b = GroupMember.objects.filter(username=name,group_name=name2,is_verified=True)
			add = '/lightshare/'+group_id+'/home/'
			chk = 'user'
			ad = GroupMember.objects.filter(username=name,group_name=name2).exclude(status=chk)

			if ad:
				ap = True
			else:
				ap = False

			if b:

				usr = User.objects.get(username=name)
				num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()

				if str == "$":

					if request.method == 'POST':
						str1 = request.POST.get("search", "")
				else:

					str1=str

				if len(str1) == 0:

					invalid = True
					count = 0

					var = {
						'session_name': name,
						'favs_list': get_fav(name),
						'invalid':invalid,
						'count':count,
						'gname': get_group_name,
						'num': num,
						'notifi': Notification.objects.filter(username=name)[:5],
						'fav': fav_group.objects.filter(username=name,group_name=name2),
						'adm': ap,
						'ur': Profile.objects.get(username=name)
					}

				else:

					invalid = False
					count = GroupArticle.objects.filter(title__icontains=str1,group_name=name2,isactive=True).count()
					pid1 = int(page_id)
					num = pid1*5
					s1=num-5

					if count>5 and pid1 !=1:
						new = True
					else:
						new = False

					if count>num:
						old = True
					else:
						old = False

					var = {
						'session_name': name,
						'favs_list': get_fav(name),
						'fav': fav_group.objects.filter(username=name,group_name=name2),
						'invalid': invalid,
						'new': new,
						'old': old,
						'count': count,
						'pid':page_id,
						'num': num,
						'notifi': Notification.objects.filter(username=name)[:5],
						'str1': str1,
						'gname': get_group_name,
						'adm': ap,
						'group':GroupArticle.objects.filter(title__icontains=str1,group_name=name2,isactive=True)[s1:num],
						'ur': Profile.objects.get(username=name)
					}

				return render_to_response("group_search.html",var, context_instance=RequestContext(request))

			else:
				address='/lightshare/'+group_id+'/profile/'
				return HttpResponseRedirect(address)
		else :
			return HttpResponseRedirect("/lightshare/userhome/")

	return HttpResponseRedirect("/lightshare/login/")

def post_edit(request,group_id=1,post_id=1):

	if request.POST:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = get_group_name.group_name
		title = request.POST["title"]
		body = request.POST['body']
		try:
			b = GroupArticle.objects.get(id=post_id,isactive=True)
		except:
			address = '/lightshare/'+group_id+'/home/'
			return HttpResponseRedirect(address)

		b.title = title
		b.body = body
		b.save()
		address = '/lightshare/'+group_id+'/'+post_id+'/'
		str1 = "You edited a <a href='"+address+"'>post</a> of "+name2+""
		recentactivity(name,str1)
		return HttpResponseRedirect(address)
	
	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		if get_group_name.isactive:
			name2 = get_group_name.group_name
			b = GroupMember.objects.filter(username=name,group_name=name2,is_verified=True)
			artl = GroupArticle.objects.get(id=post_id,isactive=True)
			chk = 'user'
			ad = GroupMember.objects.filter(username=name,group_name=name2).exclude(status=chk)

			if ad:
				ap = True
			else:
				ap = False

			if b:

				usr = User.objects.get(username=name)
				num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()

				var ={
					'session_name': name,
					'favs_list': get_fav(name),
					'gname': get_group_name,
					'article': artl,
					'num': num,
					'notifi': Notification.objects.filter(username=name)[:5],
					'fav': fav_group.objects.filter(username=name,group_name=name2),
					'adm': ap,
					'ur': Profile.objects.get(username=name)
				}
				return render_to_response("edit_post.html",var, context_instance=RequestContext(request))

			else :
				address='/lightshare/'+group_id+'/profile/'
				return HttpResponseRedirect(address)

		else :
			return HttpResponseRedirect("/lightshare/userhome/")

	return HttpResponseRedirect("/lightshare/login")


def post_delete(request,group_id=1,post_id=1):
	
	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = get_group_name.group_name
		b = GroupArticle.objects.get(id=post_id,isactive=True)
		address = '/lightshare/'+group_id+'/home/'
		b.isactive = False
		b.save()
		str1 = "You have removed a post from <a href='"+address+"'>"+name2+"</a> " 
		recentactivity(name,str1)

		return HttpResponseRedirect(address)

	return HttpResponseRedirect("/lightshare/login")

def post_pin(request,group_id=1,post_id=1):
	
	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = get_group_name.group_name
		b = GroupArticle.objects.get(id=post_id,isactive=True)
		address = '/lightshare/'+group_id+'/home/'
		b.pinned = True
		b.save()
		str1 = "You have Pinned a post on <a href='"+address+"'>"+name2+"</a> " 
		recentactivity(name,str1)

		return HttpResponseRedirect(address)

	return HttpResponseRedirect("/lightshare/login")

def post_upin(request,group_id=1,post_id=1):
	
	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = get_group_name.group_name
		b = GroupArticle.objects.get(id=post_id,isactive=True)
		address = '/lightshare/'+group_id+'/home/'
		b.pinned = False
		b.save()
		str1 = "You have unpinned a post on <a href='"+address+"'>"+name2+"</a> " 
		recentactivity(name,str1)

		return HttpResponseRedirect(address)

	return HttpResponseRedirect("/lightshare/login")

def make_adm(request,group_id=1):
	
	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = get_group_name.group_name
		user_name = ""
		address = '/lightshare/'+group_id+'/home/'

		if request.POST:
			user_name = request.POST.get('adm','')
			b = GroupMember.objects.filter(username=user_name,group_name=name2,is_verified=True)
			if b:
				a = GroupMember.objects.get(username=user_name,group_name=name2)		
				a.status='admin'
				a.save()
				str1 = "You have made "+user_name+" an admin of group <a href='"+address+"'>"+name2+"</a> " 
				recentactivity(name,str1)
				str2 = "<a href='"+address+"'>"+name+" made you an admin of group "+name2+"</a>"
				notifications(user_name,str2)
				addr = '/lightshare/'+group_id+'/dashboard/'
				return HttpResponseRedirect(addr)

		return HttpResponseRedirect(address)

	return HttpResponseRedirect("/lightshare/login")

def make_mod(request,group_id=1):
	
	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = get_group_name.group_name
		user_name = ""
		address = '/lightshare/'+group_id+'/home/'

		if request.POST:
			user_name = request.POST.get('mod','')
			b = GroupMember.objects.filter(username=user_name,group_name=name2,is_verified=True)
			if b:
				a = GroupMember.objects.get(username=user_name,group_name=name2)		
				a.status='moderator'
				a.save()
				str1 = "You have made "+user_name+" a moderator of group <a href='"+address+"'>"+name2+"</a> " 
				recentactivity(name,str1)
				str2 = "<a href='"+address+"'>"+name+" made you a moderator of group "+name2+"</a>"
				notifications(user_name,str2)
				addr = '/lightshare/'+group_id+'/dashboard/'
				return HttpResponseRedirect(addr)

		return HttpResponseRedirect(address)

	return HttpResponseRedirect("/lightshare/login")

def dashboard(request,group_id=1):
	
	if 'name' in request.session:
		name = request.session['name']
		try:
			get_group_name = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		if get_group_name.isactive:
			name2 = get_group_name.group_name
			creator = get_group_name.group_creator

			pro = Profile.objects.get(username=name)
			chk = 'user'
			ad = GroupMember.objects.filter(username=name,group_name=name2).exclude(status=chk)

			if ad:
				ap = True
			else:
				ap = False

			b = GroupMember.objects.filter(username=name,group_name=name2,is_verified=True)

			if b:

				usr = User.objects.get(username=name)
				num = Notification.objects.filter(username=name,timestamp__gt=usr.last_login).count()

				var ={
					'session_name': name,
					'creator': creator,
					'crt' : Profile.objects.filter(username=creator),
					'adm': GroupMember.objects.filter(group_name=name2,status='admin').count(),
					'mod': GroupMember.objects.filter(group_name=name2,status='moderator').count(),
					'usr': GroupMember.objects.filter(group_name=name2,is_verified=True).count(),
					'post': GroupArticle.objects.filter(group_name=name2).count(),
					'gname': get_group_name,
					'num': num,
					'notifi': Notification.objects.filter(username=name)[:5],
					'fav': fav_group.objects.filter(username=name,group_name=name2),
					'pro': pro,
					'adms': GroupMember.objects.filter(group_name=name2,status='admin'),
					'mods': GroupMember.objects.filter(group_name=name2,status='moderator'),
					'adm2': GroupMember.objects.filter(username=name,group_name=name2,status='admin'),
					'request': GroupMember.objects.filter(group_name=name2,is_verified=False),
					'ur': pro
				}
				return render_to_response("admin_panel.html",var,context_instance=RequestContext(request))

			else :
				address='/lightshare/'+group_id+'/profile/'
				return HttpResponseRedirect(address)

		else :
			return HttpResponseRedirect("/lightshare/userhome/")

	return HttpResponseRedirect("/lightshare/login")

def edit_group(request,group_id=1):

	addr = "/lightshare/"+group_id+"/dashboard"

	if request.POST:

		name = request.session['name']
		try:
			group = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')
		
		if request.FILES.get("propic"):
			group.propic = request.FILES.get("propic")
		group.save()

		return HttpResponseRedirect(addr)

	if 'name' in request.session:
		return HttpResponseRedirect(addr)

	return HttpResponseRedirect("/lightshare/login")

def delete_group(request,group_id=1):

	addr = "/lightshare/userhome/"
	addr2 = "/lightshare/"+group_id+"/dashboard"

	if 'name' in request.session:

		name = request.session['name']
		try:
			group = Group.objects.get(id=group_id)
		except:
			return HttpResponseRedirect('/lightshare/userhome/')

		name2 = group.group_name
		gm = GroupMember.objects.filter(username=name,group_name=name2,status='admin',is_verified=True)
		
		if gm:
			group.isactive=False
			group.save()

			str1 = "You have deleted group <a href='#'>"+name2+"</a>"
			str2 = "<a href='#'>Group "+name2+" has been deleted by "+name+"</a>"
			recentactivity(name,str1)
			noti = GroupMember.objects.filter(group_name=name2,is_verified=True)
			for n in noti:
				if name!=n.username:
					notifications(n.username,str2)

			fav = fav_group.objects.filter(group_name=name2)
			if fav:
				fav.delete()

			post = GroupArticle.objects.filter(group_name=name2)
			for x in post:
				x.isactive=False
				x.save()

				like = Post_Like.objects.filter(post_id=x.id)
				if like:
					like.delete()

				comment = Post_Comment.objects.filter(post_id=x.id)
				if comment:
					comment.delete()

			member = GroupMember.objects.filter(group_name=name2)
			if member:
				member.delete()

			return HttpResponseRedirect(addr)

		return HttpResponseRedirect(addr2)

	return HttpResponseRedirect("/lightshare/login")