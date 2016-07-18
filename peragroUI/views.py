from django.shortcuts import render
import os
import tempfile
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import resolve
from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect
# from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_project.models import *
# from events.models import/ EventNew
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect,Http404,HttpResponse, JsonResponse
from django.template.loader import get_template
from django.template import Context
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import difflib
import json
from django.http import JsonResponse
from example_project.settings import *
from django_project import serializers
from django_project import models

from django_project import signals
from django_project import filters as dp_filters
from exceptions import *
from damn_at import Analyzer, FileDescription, FileId, mimetypes
from damn_at.analyzer import *
from damn_at.utilities import *
from damn_at.analyzer import AnalyzerException

# def home(request):
#     return render(request,'login.html')
@csrf_exempt
def login_main(request):

	context = RequestContext(request)

	if request.method == 'POST':
		username = request.POST['login_username']
		password = request.POST['login_password']
		user = authenticate(username=username, password=password)
		if user:
			if user.is_active:
				login(request, user)
				return HttpResponsePermanentRedirect('../dashboard/'+username+'/')
			else:
				context = {'error_heading' : "Account Inactive", 'error_message' :  'Your account is currently INACTIVE'}
				return render(request, 'registration/error.html', context)
		else:
			context = {'error_heading' : "Invalid Login Credentials", 'error_message' :  'Please <a href=".">try again</a>'}
			return render(request, 'registration/error.html', context)
	else:
		error = 'POST request not sent'
		return render(request, 'login.html',{'error':error})

def user_logout(request):
    logout(request)
    return redirect('../../login/')

@csrf_exempt
@login_required
def dashboard(request, username):
	if request.user:
		self_user = request.user
		self_username = self_user.username
		username = str(username)
		if username == self_username:
			user_profile = Profile.objects.get(pk=self_user)
			user_membership = Membership.objects.filter(member=self_user)
			project_list=[]
			for x in user_membership:
				project_list.append(x.project)
			context = {
				'user_profile' : user_profile,
				'user' : self_user,
				'profile_user_membership':user_membership,
				'project_list':project_list,
			}
			return render(request, 'self_dashboard.html', context)   
	  #   elif allied_ob:
			# allied_ob = allied_ob[0]
			# exp= allied_ob.past_experiences.all()
			# rec= Recommendations.objects.filter(user=user, accepted=True)
			# l_list= locations.objects.filter(allied=allied_ob)
			# context = {
			# 	'allied' : allied_ob,
			# 	'exp' : exp,
			# 	'rec' : rec,
			# 	'user' : user,
			# 	'l_list':l_list,
			# }
			# return render(request, 'registration/dashboard_allied.html', context)
		else:
			profile_user = User.objects.get(username=username)
			user_profile = Profile.objects.get(user=profile_user)
			profile_user_membership = Membership.objects.filter(member=profile_user)
			self_user_membership = Membership.objects.filter(member=self_user)
			self_user_profile = Profile.objects.get(pk=self_user)
			project_list=[]
			for x in self_user_membership:
				project_list.append(x.project)
			context = {
				'user' : self_user,
				'user_profile' : user_profile,
				'profile_user' : profile_user,
				'profile_user_membership':profile_user_membership,
				'self_user_membership':self_user_membership,
				'self_user_profile':self_user_profile,
				'project_list':project_list,
			}
			return render(request, 'profile_dashboard.html', context)
	else:
		pass

@csrf_exempt
@login_required
def update_profile(request):
    if request.method == 'POST':
		user_ob = request.user
		user_profile = Profile.objects.get(pk=user_ob)
		user_membership = Membership.objects.filter(member=user_ob)
		user_ob.first_name = request.POST['fname']
		user_ob.last_name = request.POST['lname']
		user_profile.description = request.POST['description']
		try:
			user_profile.profile_pic= request.FILES['0']
		except:
			dumpvar=0

		user_ob.save()
		user_profile.save()
		return HttpResponse('done')

@csrf_exempt
@login_required
def project_page(request, author_name, project_slug):
	user = request.user
	user_profile = Profile.objects.get(pk=user)
	user_membership = Membership.objects.filter(member=user)
	project_list=[]
	for x in user_membership:
		project_list.append(x.project)
	author_ob = User.objects.get(username = author_name)
	project_ob = Project.objects.filter(author = author_ob, slug = project_slug)[0]
	members_list = project_ob.members.all()
	project_media = MediaUpload.objects.filter(project=project_ob)

	task_list = Task.objects.filter(project=project_ob)
	

	profile_list = []	
	for x in members_list:
		p = Profile.objects.get(pk = x)
		profile_list.append(p)
	context={
		'project_ob':project_ob,
		'profile_list':profile_list,
		'user_profile' : user_profile,
		'user' : user,
		'user_project_list':project_list,
		'project_media':project_media,
	}
	if request.method == 'POST':
		# for x in 
		media_ob = MediaUpload.objects.create(project=project_ob)
		media_ob.media = request.FILES['file']
		# media_ob.project = project_ob
		media_ob.save()
		if media_ob.media.url:
			analyzer = Analyzer()
			path = os.path.join(MEDIA_ROOT, media_ob.media.name)
			media_ob.mimetype = mimetypes.guess_type(path, False)[0]
			file_descr = analyzer.analyze_file(path)
			file_descr.hash = calculate_hash_for_file(path)
			media_ob.file_description = file_descr
			media_ob.hash = file_descr.hash
			media_ob.save()

		return HttpResponse('done')
	else:
		return render(request, 'project_page.html', context)
		# try:
		# 	artist_ob.profile_pic= request.FILES['0']
  #           except:
  #               dumpvar=0
@csrf_exempt
@login_required	
def media_view(request, mid):
	media_ob = MediaUpload.objects.get(id= mid)
	if request.method=='POST':
		comment = Comment()
		comment.author = request.user
		comment.content_type = ContentType.objects.get_for_model(media_ob)
		comment.object_pk = mid
		comment.comment = request.POST['comm-text']
		try:
			comment.annotation = str(request.POST['json-data'])
		except:
			comment.annotation = None
		comment.save()
		return HttpResponseRedirect('.')

	path = os.path.join(MEDIA_ROOT, media_ob.media.name)
	analyzer = Analyzer()
	file_descr = analyzer.analyze_file(path)
	mdesc = pretty_print_file_description(file_descr)
	comment_content_type = ContentType.objects.get_for_model(media_ob)
	comments = Comment.objects.filter(content_type__pk=comment_content_type.id, object_pk=str(mid))
	# clist = []
	# for x in comments:
	# 	userx = x.author
	# 	user_profile = Profile.objects.get(pk=userx)
	# 	clist.append(x, user_profile)
	#  fileid = FileId(filename=os.path.abspath(an_uri))
	# file_descr = FileDescription(file=fileid)
	context = {
		'mdesc':mdesc,
		'media_ob':media_ob,
		'comments':comments,
		'user':request.user,
	} 
	return render(request, 'media_image.html', context)

# @login_required
# @csrf_exempt
# def media_image(request):

# def user_validation(request, val_user): #This function validates the users and returns a value which will indicate whether a given user is the one that is loggd in or som
# 	user = RequestContextst.user
# 	if user == val_user:
# 		return
# 	else:
# 		return


# def registration(request):
#     # Like before, get the request's context.
# 	context = RequestContext(request)

#     # A boolean value for telling the template whether the registration was successful.
#     # Set to False initially. Code changes value to True when registration succeeds.
# 	registered = False

# 	# If it's a HTTP POST, we're interested in processing form data.
# 	if request.method == 'POST':
# 		choice = request.POST['choice']
#         # Attempt to grab information from the raw form information.
#         # Note that we make use of both UserForm and UserartistForm.
# 		user_form = UserForm(data=request.POST)

#         # If the two forms are valid...
# 		if user_form.is_valid():
#             # Save the user's form data to the database.
#             # emailadds = [k.email for k in User.objects.all()]
#             # if user_form.email in emailadds:
#             #   return HttpResponse('Email Address not unique')
# 			user = user_form.save()

#             # Now we hash the password with the set_password method.
#             # Once hashed, we can update the user object.
#             password= user.password
#             user.set_password(user.password)
#             user.is_active = True
#             user.save()
#             uid= user.id
#             body = "Thank You for Registering. Please Confirm your email:http://filmboard.ml/email_verify/"+ str(uid)+"/"
#             username =user.username
#             user_ob = user
#             user = authenticate(username=username, password=password)
#             send_simple_message(user.email,body)
#             login(request, user)                
#             registered = False
#             if choice == '1':
#                 artist_ob= Artist(user=user_ob,name='', location='')
#                 artist_ob.save()
#                 return HttpResponseRedirect('../updateprofile/')
#                 # return render(request, 'registration/.html',{'a_form': artist_form, 'registered': registered, 'choice' : '1' })
#                 # artist_registration(request)
#             elif choice == '2':
#                 allied_ob= Allied(user=user_ob,name='',location='')
#                 allied_ob.save()
#                 return HttpResponseRedirect('../updateprofile/')
#             elif choice == '3':
#                 prod_ob= Production(user=user_ob,name='', location='')
#                 prod_ob.save()
#                 return HttpResponseRedirect('../updateprofile/')
#         else:
#             print user_form.errors

#     # Not a HTTP POST, so we render our form using two ModelForm instances.
#     # These forms will be blank, ready for user input.
#     else:
#         user_form = UserForm()
#         error = 'Server side error'
#         return render(request, 'registration/registration1.html', {'user_form' :user_form, 'error':error})
#     # Render the template depending on the context.
#     # return render(request, 'registration/register.html',
#     #         {'user_form': user_form, 'artist_form': artist_form, 'registered': registered})


# Create your views here.