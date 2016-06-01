from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import notifications.urls


from django_project.urls import router

import follow.views
import rest_framework.urls
import rest_framework.authtoken.views

urlpatterns = [
    url(r'^', include(router.urls)),

    url(r'^api-auth/', include(rest_framework.urls, namespace='rest_framework')),
    url(r'^api-token-auth/', rest_framework.authtoken.views.obtain_auth_token),

    url(r'^admin/', include(admin.site.urls)),

]

urlpatterns += [
    url('^inbox/notifications/', include(notifications.urls, namespace='notifications')),
    url(r'^toggle/(?P<app>[^\/]+)/(?P<model>[^\/]+)/(?P<id>\d+)/$', follow.views.toggle, name='toggle'),
    url(r'^toggle/(?P<app>[^\/]+)/(?P<model>[^\/]+)/(?P<id>\d+)/$', follow.views.toggle, name='follow'),
    url(r'^toggle/(?P<app>[^\/]+)/(?P<model>[^\/]+)/(?P<id>\d+)/$', follow.views.toggle, name='unfollow'),
    url(r'^', include('django_project.urls')),
    url(r'^', include('peragroUI.urls')),

]
