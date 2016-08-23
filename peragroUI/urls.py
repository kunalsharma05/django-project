from django.conf.urls import include, url
from peragroUI import views
from example_project import settings
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns



urlpatterns = [
    # url(r'^$', views.index),
    url(r'^login/$', views.login_main),
    url(r'^dashboard/(?P<username>\w+)/$', views.dashboard, name='dashboard'),
    url(r'^updateprofile/$', views.update_profile, name='update profile'),
    url(r'^logout/$', views.user_logout, name='logout'),
    # url(r'^register/$', views.register),
    url('^project/(?P<author_name>\w+)/(?P<project_slug>[^/]+)/$', views.project_page, name='projects'),
    # url(r'^profile/edit/$', views.edit_profile),
    # url(r'^profile/help/$', views.profile_help),
	url(r'^media/(?P<mid>[0-9]+)/$', views.media_view, name='media review'),
    url(r'^media_description/(?P<mid>[0-9]+)/$', views.media_description, name='media description'),


    # url(r'^questions/$', views.questions),
    # url(r'^query/$', views.query),
    # url(r'^survey_submit/$', views.survey_submit),
    # url(r'^surveys/add/$', views.add_survey),


    # url(r'^survey_view/$', views.view_surveys),

    # url(r'^survey_view/$', views.view_surveys),

    url(r'^gantt_data/(?P<pid>[0-9]+)/$', views.get_gantt_data),
    url(r'^gantt/(?P<pid>[0-9]+)/$', views.ganttview),

    # url(r'^diary/$', views.diary),
    # url(r'^dashboard/(?P<user_id>[0-9]+)/$', views.coach_user_profile),
    # url(r'^coachlist/$', views.approved_coaches),

    
    # url(r'^test/$', views.test_pic),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)