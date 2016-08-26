from django.shortcuts import render
import os
import time
import tempfile
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import resolve
from django.template import RequestContext
from django.shortcuts import render, render_to_response, redirect
# from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django_project.models import *
from peragroUI.models import *

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
import datetime
from django_project import signals
from django_project import filters as dp_filters
from exceptions import *
from damn_at import Analyzer, FileDescription, FileId, mimetypes, Transcoder
from damn_at.analyzer import *
from damn_at.utilities import *
from damn_at.analyzer import AnalyzerException
import ast
from actstream import action
from actstream.models import Action
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
			news_feed = Action.objects.all()
			project_list=[]
			for x in user_membership:
				project_list.append(x.project)
			context = {
				'user_profile' : user_profile,
				'user' : self_user,
				'profile_user_membership':user_membership,
				'project_list':project_list,
				'news_feed':news_feed,
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
	roles = Role.objects.filter(project = project_ob)
	task_list = TaskUI.objects.filter(project=project_ob)
	relation_list = AssignedResource_Relation.objects.filter(project = project_ob)
	priority_list = Priority.objects.filter(project=project_ob)
	type_list = TaskType.objects.filter(project=project_ob)



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
		'roles':roles,
		'members_list':members_list,
		'task_list':task_list,
		'relation_list':relation_list,
		'type_list':type_list,
		'priority_list':priority_list,
	}
	if request.method == 'POST':
		# for x in 
		if request.POST.get('update-role'):
			role = Role.objects.get(id = int(request.POST['id']))
			role.name = request.POST['name']
			role.save()
			return HttpResponseRedirect('.')

		elif request.POST.get('delete-role'):
			role = Role.objects.get(id = int(request.POST['id']))
			role.delete()
			return HttpResponseRedirect('.')

		elif request.POST.get('new-role'):
			role = Role()
			role.name = request.POST['name']
			role.project = project_ob
			role.save()
			return HttpResponseRedirect('.')
		
		elif request.POST.get('update-rel'):
			rel = AssignedResource_Relation.objects.get(id = int(request.POST['id']))
			rel.task = TaskUI.objects.get(id = int(request.POST['task']))
			rel.user = User.objects.get(id = int(request.POST['user']))
			rel.role = Role.objects.get(id = int(request.POST['role']))
			rel.effort = request.POST['effort'] 
			rel.save()
			return HttpResponseRedirect('.')

		elif request.POST.get('delete-rel'):
			rel = AssignedResource_Relation.objects.get(id = int(request.POST['id']))
			rel.delete()
			return HttpResponseRedirect('.')

		elif request.POST.get('new-rel'):
			rel = AssignedResource_Relation.objects.get(id = int(request.POST['id']))
			rel.task = TaskUI.objects.get(id = int(request.POST['task']))
			rel.user = User.objects.get(id = int(request.POST['user']))
			rel.role = Role.objects.get(id = int(request.POST['role']))
			rel.effort = request.POST['effort'] 
			rel.project = project_ob
			rel.save()
			return HttpResponseRedirect('.')
	
		elif request.POST.get('update-task'):	
			task = TaskUI.objects.get(id = int(request.POST['id']))
			task.name = request.POST['name']
			task.short_name = request.POST['short-name']
			task.level = request.POST['level']
			task.summary = request.POST['summary']
			task.description = request.POST['description']
			task.status = request.POST['status']
			task.priority = Priority.objects.get(id = int(request.POST['priority']))
			task.type = TaskType.objects.get(id = int(request.POST['type']))
			if request.POST.get('start-is-milestone'):
				task.start_is_milestone = True
			else:
				pass
			if request.POST.get('end-is-milestone'):
				task.end_is_milestone = True
			else:
				pass
			if request.POST.get('has-child'):
				task.start_is_milestone = True
			else:
				pass
			if request.POST.get('can-write'):
				task.start_is_milestone = True
			else:
				pass
			task.depends = request.POST['depends']
			task.save()
			return HttpResponseRedirect('.')

		elif request.POST.get('del-task'):	
			task = TaskUI.objects.get(id = int(request.POST['id']))
			task.delete()
			return HttpResponseRedirect('.')

		elif request.POST.get('update-task'):	
			task = TaskUI.objects.get(id = int(request.POST['id']))
			task.name = request.POST['name']
			task.short_name = request.POST['short-name']
			task.level = request.POST['level']
			task.summary = request.POST['summary']
			task.description = request.POST['description']
			task.status = request.POST['status']
			task.priority = Priority.objects.get(id = int(request.POST['priority']))
			task.type = TaskType.objects.get(id = int(request.POST['type']))
			if request.POST.get('start-is-milestone'):
				task.start_is_milestone = True
			else:
				pass
			if request.POST.get('end-is-milestone'):
				task.end_is_milestone = True
			else:
				pass
			if request.POST.get('has-child'):
				task.start_is_milestone = True
			else:
				pass
			if request.POST.get('can-write'):
				task.start_is_milestone = True
			else:
				pass
			task.depends = request.POST['depends']
			task.save()
			return HttpResponseRedirect('.')

		elif request.POST.get('del-task'):	
			task = TaskUI.objects.get(id = int(request.POST['id']))
			task.delete()
			return HttpResponseRedirect('.')

		elif request.POST.get('new-task'):	
			task = TaskUI()
			task.name = request.POST['name']
			task.short_name = request.POST['short-name']
			task.project = request.POST['project']
			task.author = request.POST['author']
			task.level = request.POST['level']
			task.summary = request.POST['summary']
			task.description = request.POST['description']
			task.status = request.POST['status']
			task.priority = Priority.objects.get(id = int(request.POST['priority']))
			task.type = TaskType.objects.get(id = int(request.POST['type']))
			task.project = project_ob
			task.author = request.user
			if request.POST.get('start-is-milestone'):
				task.start_is_milestone = True
			else:
				pass
			if request.POST.get('end-is-milestone'):
				task.end_is_milestone = True
			else:
				pass
			if request.POST.get('has-child'):
				task.start_is_milestone = True
			else:
				pass
			if request.POST.get('can-write'):
				task.start_is_milestone = True
			else:
				pass
			task.depends = request.POST['depends']
			task.save()
			return HttpResponseRedirect('.')

		# elif request.POST.get() 
			# for key in request.POST.iterkeys():
			# 	v
			# 	if key == 'new_role':
			# 		if request.POST[key] != "":
			# 			role = Role()
			# 			role.name = request.POST[key]
			# 			role.project = project_ob
			# 			role.save()
			# 		else:
			# 			pass
			# 	elif key == 'save_role':
			# 		pass
			# 	else:
			# 		role.name = request.POST[key]
			# 		role.save()
		
		# elif request.POST.get('save_relation'):
		# 	flag = 0
		# 	for key in request.POST.iterkeys():
		# 		if key in ['new_task','new_role','new_effort','new_user']:
		# 			if flag == 0:
		# 				if request.POST.get('add_new_relation'):	
		# 					flag = 1
		# 					rel = AssignedResource_Relation()
		# 					rel.project = project_ob
		# 					rel.task = TaskUI.objects.get(id = int(request.POST['new_task']))
		# 					rel.user = User.objects.get(id = int(request.POST['new_user']))
		# 					rel.role = Role.objects.get(id = int(request.POST['new_role']))
		# 					rel.effort = request.POST['new_effort'] 
		# 					action.send(rel.user, verb='assigned', action_object=rel.role, target=rel.task)
		# 					rel.save()
		# 				else:
		# 					pass
		# 		elif key == 'save_relaltion':
		# 			pass
		# 		else:
		# 			for rel in relation_list:
		# 				if str(rel.id) == key:
		# 					rel.task = TaskUI.objects.get(id = int(request.POST[key]))
		# 					rel.role = Role.objects.get(id = int(request.POST[key+'_role']))
		# 					rel.user = User.objects.get(id = int(request.POST[key+'_user']))
		# 					rel.effort = int(request.POST[key+'_effort'])
							# rel.save()

			# if request.POST.get('save_reelaltion'):
								# for x in roles:
			# 	try:
			# 		role = Role.objects.get(id = int(request.POST[x.id]))
			# 		role.name = 
			# 	role.	
		
		else:
			media_ob = MediaUpload.objects.create(project=project_ob)
			media_ob.media = request.FILES['file']
		# media_ob.project = project_ob
			media_ob.save()
			if media_ob.media.url:
				analyzer = Analyzer()
				path = os.path.join(MEDIA_ROOT, media_ob.media.name)
				media_ob.mimetype = mimetypes.guess_type(path, False)[0]
				file_descr = analyzer.analyze_file(path)
				print(file_descr)
				file_descr.hash = calculate_hash_for_file(path)
				media_ob.file_description = file_descr
				media_ob.hash = file_descr.hash
				media_ob.save()
				action.send(request.user, verb='uploaded', action_object=media_ob, target=project_ob)
				# if 'video' in media_ob.mimetype:	
				# 	transcdoer_path = MEDIA_ROOT
				# 	transcoder = Transcoder(transcdoer_path)
				# 	asset_name = get_asset_names_in_file_descr(file_descr)
				# 	asset_name = asset_name[0]
				# 	asset_id = find_asset_ids_in_file_descr(file_descr, asset_name)
				# 	asset_id = asset_id[0]
				# 	target_mimetype = transcoder.get_target_mimetype(media_ob.mimetype, 'image/jpeg')	
				# 	height = file_descr.assets[0].metadata['height'].int_value
				# 	width = file_descr.assets[0].metadata['width'].int_value
				# 	duration = file_descr.assets[0].metadata['duration'].string_value					
				# 	new_width = 200
				# 	new_height = 200*(height/width)
				# 	try:
				# 		time = duration.split(':')
				# 		time = eval(time[0])*3600 + eval(time[1])*60 + eval(time[2])
				# 	except:
				# 		time = duration.split('.')
				# 		time = eval(time[0])
				# 	if time < 10:
				# 		options = {'second':-1,'size':(new_width,new_height)}
				# 	else:
				# 		options = {'second':5,'size':(new_width,new_height)}
				# 	get_image = transcoder.transcode(file_descr, asset_id, target_mimetype, **options)
				# 	media_ob.resource_link = get_image[0]
				# 	media_ob.save()				 

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
		comment = UiComment()
		comment.author = request.user
		comment.content_type = ContentType.objects.get_for_model(media_ob)
		comment.object_pk = mid
		comment.comment = request.POST['comm-text']
		try:
			comment.annotation = str(request.POST['json-data'])
		except:
			comment.annotation = None
		comment.save()
		action.send(request.user, verb='commented', action_object=comment, target=media_ob)
		return HttpResponseRedirect('.')

	path = os.path.join(MEDIA_ROOT, media_ob.media.name)
	analyzer = Analyzer()
	file_descr = analyzer.analyze_file(path)
	mdesc = pretty_print_file_description(file_descr)
	comment_content_type = ContentType.objects.get_for_model(media_ob)
	comments = UiComment.objects.filter(content_type__pk=comment_content_type.id, object_pk=str(mid))
	
	# if media_ob.mimetype == 'image/jpeg':

	context = {
		'mdesc':mdesc,
		'file_descr':file_descr,
		'media_ob':media_ob,
		'comments':comments,
		'user':request.user,
	} 
	if 'video' in media_ob.mimetype:
		return render(request, 'media_video.html', context)
	elif 'image' in media_ob.mimetype:
		return render(request, 'media_image.html', context)

@csrf_exempt
@login_required	
def media_description(request, mid):
	media_ob = MediaUpload.objects.get(id= mid)
	path = os.path.join(MEDIA_ROOT, media_ob.media.name)
	analyzer = Analyzer()
	file_descr = analyzer.analyze_file(path)
	data = {}
	data['hash']=media_ob.hash
	data['assets'] = []
	if file_descr.assets:
		for x in file_descr.assets:
			asset_data = {}
			asset_data['subname'] = x.asset.subname
			asset_data['mimetype'] = x.asset.mimetype
			asset_data['dependencies'] = []
			if x.dependencies:
				for y in x.dependencies:
					dep_data = {}
					dep_data['subname'] = y.subname
					dep_data['mimetype'] = y.mimetype
					asset_data['dependencies'].append(dep_data)
			asset_data['metadata'] = []
			if x.metadata:
				for key, value in x.metadata.items():
					metadata_data = {}
					type, val = get_metadatavalue_type(value)
					print(val)
					metadata_data['key'] = key
					metadata_data['type'] = type
					metadata_data['val'] = val
					asset_data['metadata'].append(metadata_data)
			data['assets'].append(asset_data)

	return JsonResponse(data)

	# clist = []
	# for x in comments:
	# 	userx = x.author
	# 	user_profile = Profile.objects.get(pk=userx)
	# 	clist.append(x, user_profile)
	#  fileid = FileId(filename=os.path.abspath(an_uri))
	# file_descr = FileDescription(file=fileid)

@csrf_exempt
@login_required	
def get_gantt_data(request, pid):
	# print('hi')
	project = Project.objects.get(id = pid)
	tasks = TaskUI.objects.filter(project=project)
	if request.method=='POST':
	# try:
		# post_data =request.GET
		# print(post_data)
	# except:	
		# print('poop')
		p_data = json.loads(request.POST['project'])
		for x in p_data['tasks']:
			for y in tasks:
				if y.id == x['id']:
					y.name = x['name']
					y.short_name=x['code']
					y.level=x['level']
					y.status=x['status']
					y.can_write=x['canWrite']
					y.start = datetime.fromtimestamp(int(x['start'])/1000).date()
					y.end = datetime.fromtimestamp(int(x['end'])/1000).date()
					print(datetime.fromtimestamp(int(x['end'])/1000).date())
					y.start_is_milestone = x['startIsMilestone']
					y.end_is_milestone = x['endIsMilestone']
					y.depends = x['depends']
					y.collapsed = x['collapsed']
					y.has_child = x['hasChild']
					y.type = TaskType.objects.get(id = int(x['type']))
					y.save()
					assigned_list = []
					list_from_json = []

					for a in AssignedResource_Relation.objects.filter(task=y):
						assigned_list.append(a.id)
					for i in x['assigs']:
						list_from_json.append(int(i['id']))
						if i['id'] in assigned_list:
							print(int(i['id']))
							z = AssignedResource_Relation.objects.get(id = int(i['id']))
							z.user = User.objects.get(id = int(i['resourceId']))
							z.role = Role.objects.get(id = int(i['roleId']))
							z.effort = i['effort']
							z.save()
							# x['assigs'].remove(i)
						elif i['id'] not in assigned_list:
							print('hi',i['id'])
							z = AssignedResource_Relation()
							z.task = y
							z.user = User.objects.get(id = int(i['resourceId']))
							z.role = Role.objects.get(id = int(i['roleId']))
							z.project = project
							z.effort = i['effort']
							z.save()	
							# x['assigs'].remove(i)
					
					for a in assigned_list:
						if a not in list_from_json:
							z = AssignedResource_Relation.objects.get(id = a)
							z.delete()
		return JsonResponse({'saved':'saved'})
		# for x in post_data['tasks']:
			# print x['id']

	data = {}
	data['tasks']=[]
	for x in tasks:
		task_data = {}
		task_data['sex']='female'
		task_data['id']=x.id
		task_data['name']=x.name
		task_data['type']=x.type.id
		task_data['code']=x.short_name
		task_data['level']=x.level
		task_data['status']=x.status
		task_data['canWrite']=x.can_write
		task_data['start'] = int(time.mktime(x.start.timetuple())*1000)
		# task_data['end']= int(time.mktime(x.end.timetuple())*1000)
		dt = x.end-x.start
		task_data['duration']= dt.days+1
		print(x.start,x.end,dt.days)
		task_data['startIsMilestone']= x.start_is_milestone
		task_data['endIsMilestone']= x.end_is_milestone
		task_data['depends']=x.depends
		task_data['collapsed']=x.collapsed
		task_data['hasChild']=x.has_child
		assig_list=[]
		for y in AssignedResource_Relation.objects.filter(task=x):
			assig_dict={}
			assig_dict['resourceId']=y.user.id
			assig_dict['id']=y.id
			assig_dict['roleId']=y.role.id
			assig_dict['effort']=y.effort
			assig_list.append(assig_dict)
		task_data['assigs']= assig_list
		data['tasks'].append(task_data)
	data['selectedRow']=0
	data['canWrite']=True
	data['canWriteOnParent'] = True
	data['resources'] = []
	data['roles'] = []
	resource_users = project.members.all()
	for y in resource_users:
		res_dict = {}
		res_dict['id'] = y.id
		res_dict['name'] =y.username
		data['resources'].append(res_dict)
	roles = Role.objects.filter(project = project)
	for y in roles:
		roles_dict = {}
		roles_dict['id']=y.id
		roles_dict['name']=y.name
		data['roles'].append(roles_dict)
	return JsonResponse(data)

@csrf_exempt
@login_required	
def ganttview(request, pid):
	project = Project.objects.get(id = pid)
	task_type_list =  TaskType.objects.filter(project =project)
	return render(request,'gantt.html',{'id':pid, 'task_type_list':task_type_list})	



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