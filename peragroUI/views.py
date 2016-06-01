from django.shortcuts import render
import os
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

from django_project import serializers
from django_project import models

from django_project import signals
from django_project import filters as dp_filters

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
			context = {
				'user_profile' : user_profile,
				'user' : self_user,
				'profile_user_membership':user_membership,
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
			user_profile = Profile.objects.get(pk=username)
			profile_user = user_profile.user
			profile_user_membership = Membership.objects.filter(member=profile_user)
			context = {
				'user' : self_user,
				'user_profile' : user_profile,
				'profile_user' : profile_user,
				'profile_user_membership':profile_user_membership,
			}
			return render(request, 'profile_dashboard.html', context)
	else:
		pass
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
