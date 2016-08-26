from __future__ import unicode_literals

from django.db import models

# Create your models here.
import datetime
import os
from django.db import models
from django.contrib.auth.models import User, Group, AnonymousUser, Permission
from example_project.settings import *
from django.utils.translation import ugettext_lazy as __
from django.utils.translation import ugettext as _
from example_project.settings import *
from autoslug import AutoSlugField

from smart_selects.db_fields import ChainedForeignKey
from django_project.models import *

from thrift.protocol.TJSONProtocol import TJSONProtocol
from damn_at.serialization import SerializeThriftMsg, DeserializeThriftMsg
from damn_at import AssetDescription, FileDescription
from damn_at.utilities import unique_asset_id_reference_from_fields

class TaskUI(models.Model):
    """
    """
    name = models.CharField(max_length=256, null=True, blank=True)
    short_name = models.CharField(max_length=126, null=True, blank=True)
    project = models.ForeignKey(Project, verbose_name=_('project'))
    author = models.ForeignKey(User, verbose_name=_('author'), blank=True)  
    level = models.IntegerField(null=True)
    summary = models.CharField(_('summary'), max_length=64)
    description = models.TextField(_('description'))
    status = models.CharField(max_length=256, default='STATUS_ACTIVE')
    # status = ChainedForeignKey(Status, chained_field="project", chained_model_field="project", verbose_name=_('status'))
    priority = ChainedForeignKey(Priority, chained_field="project", chained_model_field="project", verbose_name=_('priority'))
    type = ChainedForeignKey(TaskType, chained_field="project", chained_model_field="project", verbose_name=_('task type'))

    start = models.DateField(_('start'), null=True, blank=True, help_text='YYYY-MM-DD')
    end = models.DateField(_('end'), null=True, blank=True, help_text='YYYY-MM-DD')

    start_is_milestone = models.BooleanField(default=False)
    end_is_milestone = models.BooleanField(default=False)
    can_write = models.BooleanField(default=True)
    has_child = models.BooleanField(default=False)
    depends = models.CharField(max_length=256,blank=True,null=True)
    collapsed = models.BooleanField(default=False)
    # milestone = ChainedForeignKey(Milestone, chained_field="project", chained_model_field="project", verbose_name=_('milestone'), null=True, blank=True)
    # component = ChainedForeignKey(Component, chained_field="project", chained_model_field="project", verbose_name=_('component'))

    created_at = models.DateTimeField(_('created at'), auto_now_add=True, editable=False)

    def __unicode__(self):
        return u'%s' % (self.name)


class Role(models.Model):
    project = models.ForeignKey(Project, verbose_name=_('project'))
    name = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return self.name

class AssignedResource_Relation(models.Model):
    task = models.ForeignKey(TaskUI)
    user = models.ForeignKey(User)
    role = models.ForeignKey(Role)
    effort = models.IntegerField(null=True, default=0)
    project = models.ForeignKey(Project, verbose_name=_('project'))
    def __unicode__(self):
            return self.task.project.name+':'+self.task.name+' '+self.user.username

def upload_manager(instance, filename):
	user = instance.project.author
	user_profile = Profile.objects.get(user=user)
	user_organisation = user_profile.organisation
	user_project = instance.project.name
	# b = str(MEDIA_ROOT)
	a = user_organisation+'/'+user_project+'/'+filename+'/'
	return a
	return MEDIA_ROOT

class MediaUpload(models.Model):
    project = models.ForeignKey(Project, related_name='files_project', on_delete=models.CASCADE)
	# owner = models.ForeignKey(User, on_delete=models.CASCADE)
    media = models.FileField(upload_to=upload_manager)
    resource_link = models.CharField(max_length = 1024, null=True)
    mimetype = models.CharField(max_length=255, null=True, blank=True)
    file_description = models.TextField()
    hash = models.CharField(max_length=128, db_index=True)
    def __unicode__(self):
        return 'File: %s %s'%(self.media.name, self.mimetype)

class Profile(models.Model):
    """
    """    
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    description = models.TextField()
    profile_pic = models.ImageField(upload_to = 'profile_pictures/', default = 'profile_pictures/user.png')
    organisation = models.CharField(max_length=256, blank=False)
    position = models.CharField(blank=True, max_length=128)
    def __unicode__(self):
        return self.user.username

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django_project.managers import CommentManager
from django.contrib.contenttypes.models import ContentType

COMMENT_MAX_LENGTH = getattr(settings, 'COMMENT_MAX_LENGTH', 3000)

class UiComment(models.Model):
    """
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'))

    content_type = models.ForeignKey(ContentType,
            verbose_name=_('content type'),
            related_name="content_type_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    comment = models.TextField(_('comment'), max_length=COMMENT_MAX_LENGTH)
    annotation = models.TextField(null=True)
    # Metadata about the comment
    submit_date = models.DateTimeField(_('date/time submitted'), auto_now_add=True, editable=False)

    # Manager
    objects = CommentManager()

    class Meta:
        ordering = ('-submit_date',)
        permissions = [("can_moderate", "Can moderate comments")]
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return "%s" % (self.comment[:50])

# class AssetsMedia(models.Model):
	
# 	file = models.ForeignKey(MediaUpload, related_name='assets', on_delete=models.CASCADE)
# 	subname = models.CharField(max_length=255)
# 	mimetype = models.CharField(max_length=255, null=True, blank=True)
# 	asset_description = models.TextField()
# 	def __unicode__(self):
# 		return 'AssetReference: %s %s'%(self.subname, self.mimetype)

# class DependenciesRelation(models.Model):
# 	file = models.ForeignKey(MediaUpload, on_delete=models.CASCADE)
# 	asset = models.ForeignKey(AssetsMedia, related_name='asset')
# 	dependency = models.ForeignKey(AssetsMedia, related_name='dependency')
# 	def __unicode__(self):
# 		return 'Dependency of %s : %s'%(self.asset.subname, self.dependency.subname)

# class Annotation(models.Model):
# 	comment = models.OneToOneField(Comment, on_delete=models.CASCADE)
	
# 	# aspect_ratio = models.DecimalField(max_digits=5, decimal_places=3)
# 	def __unicode__(self):
# 		return str(self.comment)111111111111111111