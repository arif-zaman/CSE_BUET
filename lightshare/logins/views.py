from django.shortcuts import render, render_to_response, RequestContext
from django.http import HttpResponseRedirect
from django.contrib import auth
from profiles.models import Profile
from django.contrib.auth.models import User
from django.core.context_processors import csrf


def login(request):
    if 'name' in request.session:
        name = request.session['name']
        return HttpResponseRedirect("/lightshare/userhome/")

    c = {}
    c.update(csrf(request))
    return render_to_response("login.html", c)


def auth_view(request):
    if 'name' in request.session:
        name = request.session['name']
        return HttpResponseRedirect("/lightshare/userhome/")

    email = request.POST.get("email", "")
    password = request.POST.get("password", "")

    usr = Profile.objects.filter(email=email)
    username = ""
    for u in usr:
        username = u.username

    user = auth.authenticate(username=username, password=password)

    if user is not None:

        request.session['name'] = username
        auth.login(request, user)
        return HttpResponseRedirect("/lightshare/loggedin/")
    else:
        return HttpResponseRedirect("/lightshare/invalid/")


def loggedin(request):
    if 'name' in request.session:
        name = request.session['name']
        return HttpResponseRedirect("/lightshare/userhome/")

    return HttpResponseRedirect("/lightshare/login")


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/lightshare.com/")


def invalid_login(request):
    if 'name' in request.session:
        name = request.session['name']
        return HttpResponseRedirect("/lightshare/userhome/")

    return render_to_response("invalid_login.html")