from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

def about(request):

	if 'name' in request.session:
		name = request.session['name']
		return HttpResponseRedirect("/lightshare/username")

	return render_to_response("about.html")

def welcome(request):

	if 'name' in request.session:
		name = request.session['name']
		return HttpResponseRedirect("/lightshare/username")

	return render_to_response("welcome.html")

def privacy(request):

	if 'name' in request.session:
		name = request.session['name']
		return HttpResponseRedirect("/lightshare/username")

	return render_to_response("terms.html")

def term(request):

	if 'name' in request.session:
		name = request.session['name']
		return HttpResponseRedirect("/lightshare/username")

	return render_to_response("terms.html")