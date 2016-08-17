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

from django_project.mixins import ProjectMixin, TaskMixin, CommentMixin

from thrift.protocol.TJSONProtocol import TJSONProtocol
from damn_at.serialization import SerializeThriftMsg, DeserializeThriftMsg
from damn_at import AssetDescription, FileDescription
from damn_at.utilities import unique_asset_id_reference_from_fields


class Project(ProjectMixin, models.Model):
    """
    """
    name = models.CharField(_('name'), max_length=64)
    slug = AutoSlugField(max_length=128, populate_from='name', unique_with='author')

    description = models.TextField(null=True, blank=True)

    author = models.ForeignKey(User, name=_('author'), related_name='created_projects')

    members = models.ManyToManyField(User, verbose_name=_('members'), through="Membership")

    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    modified_at = models.DateTimeField(_('modified at'), auto_now=True)


    class Meta:
        #verbose_name = _('project')
        #verbose_name_plural = _('projects')
        #ordering = ['name']
        #get_latest_by = 'created_at'
        #unique_together = ['author', 'name']
        permissions = (
            ('view_project', 'Can view project'),
            ('admin_project', 'Can administer project'),
            ('can_read_repository', 'Can read repository'),
            ('can_write_to_repository', 'Can write to repository'),
            ('can_add_task', 'Can add task'),
            ('can_change_task', 'Can change task'),
            ('can_delete_task', 'Can delete task'),
            ('can_view_tasks', 'Can view tasks'),
            ('can_add_member', 'Can add member'),
            ('can_change_member', 'Can change member'),
            ('can_delete_member', 'Can delete member'),
        )

    def __unicode__(self):
        return self.name

class Component(models.Model):
    """
    """
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=64)
    slug = AutoSlugField(max_length=64, populate_from='name', always_update=True, unique_with='project')
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = _('component')
        verbose_name_plural = _('components')
        ordering = ('name',)
        unique_together = ('project', 'name')

    def __unicode__(self):
        return self.project.name+': '+self.name

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

class Membership(models.Model):
    """
    """
    member = models.ForeignKey(User, verbose_name=_('member'))
    project = models.ForeignKey(Project, verbose_name=_('project'))
    joined_at = models.DateTimeField(_('joined at'), auto_now_add=True)

    def __unicode__(self):
        return u"%s@%s" % (self.member, self.project)

    class Meta:
        unique_together = ('project', 'member')


# class Milestone(models.Model):
#     """
#     """
#     project = models.ForeignKey(Project, verbose_name=_('project'))
#     name = models.CharField(max_length=64)
#     slug = AutoSlugField(max_length=64, populate_from='name', always_update=True, unique_with='project')
#     description = models.TextField()
#     author = models.ForeignKey(User, verbose_name=_('author'))
#     created_at = models.DateTimeField(_('created at'), auto_now_add=True)
#     modified_at = models.DateTimeField(_('modified at'), auto_now=True)
#     deadline = models.DateField(_('deadline'), default=datetime.date.today() + datetime.timedelta(days=10))
#     date_completed = models.DateField(_('date completed'), null=True, blank=True)

#     class Meta:
#         ordering = ('created_at',)
#         verbose_name = _('milestone')
#         verbose_name_plural = _('milestones')
#         unique_together = ('project', 'name')

#     def __unicode__(self):
#         return self.project.name+': '+self.name


class DictModel(models.Model):
    name = models.CharField(_('name'), max_length=32)
    description = models.TextField(_('description'), null=True, blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ('id',)


class OrderedDictModel(DictModel):
    """
    DictModel with order column and default ordering.
    """
    order = models.IntegerField(_('order'))

    class Meta:
        abstract = True
        ordering = ['order', 'name']


class Priority(OrderedDictModel):
    """
    """
    project = models.ForeignKey(Project)
    slug = AutoSlugField(max_length=64, populate_from='name', always_update=True, unique_with='project')

    class Meta:
        verbose_name = _('priority level')
        verbose_name_plural = _('priority levels')
        unique_together = ('project', 'name')

    def __unicode__(self):
        return self.project.name+': '+self.name


class TransitionChainedForeignKeyQuerySet(models.Manager):
    def filter(self, **kwargs):
        if 'project' in kwargs:
            kwargs['project'] = self.model.objects.get(pk=kwargs['project']).project.pk
        return super(TransitionChainedForeignKeyQuerySet, self).filter(**kwargs)


class Status(OrderedDictModel):
    """
    """
    project = models.ForeignKey(Project)
    is_resolved = models.BooleanField(verbose_name=_('is resolved'), default=False)
    is_initial = models.BooleanField(verbose_name=_('is initial'), default=False)
    destinations = models.ManyToManyField('self', verbose_name=_('destinations'), through='Transition', symmetrical=False, blank=True)
    slug = AutoSlugField(max_length=64, populate_from='name', always_update=True, unique_with='project')

    objects = models.Manager()
    special = TransitionChainedForeignKeyQuerySet()

    def can_change_to(self, new_status):
        """
        Checks if ``Transition`` object with ``source`` set to ``self`` and
        ``destination`` to given ``new_status`` exists.
        """
        try:
            Transition.objects.only('id')\
                .get(source__id=self.id, destination__id=new_status.id)
            return True
        except Transition.DoesNotExist:
            return False

    class Meta:
        verbose_name = _('status')
        verbose_name_plural = _('statuses')
        unique_together = ('project', 'name')
        ordering = ['order']

    def __unicode__(self):
        return self.project.name+': '+self.name

class ChainedForeignKeyTransition(ChainedForeignKey):

    def formfield(self, **kwargs):
        defaults = {
            #'queryset': self.rel.to._default_manager.complex_filter(self.rel.limit_choices_to),
            'queryset': self.rel.to.special.complex_filter(self.rel.limit_choices_to),
            'manager': 'special',
        }
        defaults.update(kwargs)
        return super(ChainedForeignKeyTransition, self).formfield(**defaults)

class Transition(models.Model):
    """
    Instances allow to change source Status to destination Status.
    Needed for custom workflows.
    """
    source = models.ForeignKey(Status, verbose_name=_('source status'), related_name='sources')
    destination = ChainedForeignKeyTransition(Status, chained_field="source", chained_model_field="project", verbose_name=_('destination status'))

    class Meta:
        verbose_name = _('transition')
        verbose_name_plural = _('transitions')
        unique_together = ('source', 'destination')

    def __unicode__(self):
        return u'%s->%s' % (self.source, self.destination)


class TaskType(OrderedDictModel):
    """
    """
    project = models.ForeignKey(Project)

    class Meta:
        verbose_name = _('task type')
        verbose_name_plural = _('task types')
        unique_together = ('project', 'name')

    def __unicode__(self):
        return self.project.name+': '+self.name


class Task(TaskMixin, models.Model):
    """
    """
    name = models.CharField(max_length=256, null=True, blank=True)
    short_name = models.CharField(max_length=126, null=True, blank=True)
    project = models.ForeignKey(Project, verbose_name=_('project'))

    author = models.ForeignKey(User, verbose_name=_('author'), related_name='created_tasks', blank=True)
    
    owner = models.ForeignKey(User, verbose_name=_('owner'), related_name='owned_tasks', null=True, blank=True)
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
    component = ChainedForeignKey(Component, chained_field="project", chained_model_field="project", verbose_name=_('component'))

    created_at = models.DateTimeField(_('created at'), auto_now_add=True, editable=False)

    def __unicode__(self):
        return u'%s' % (self.summary)


class Role(models.Model):
    project = models.ForeignKey(Project, verbose_name=_('project'))
    name = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return self.project.name+':'+self.name

class AssignedResource_Relation(models.Model):
    task = models.ForeignKey(Task)
    user = models.ForeignKey(User)
    role = models.ForeignKey(Role)
    effort = models.BigIntegerField(null=True)
    def __unicode__(self):
            return self.task.project.name+':'+self.task.name+' '+self.user.username




from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django_project.managers import CommentManager
from django.contrib.contenttypes.models import ContentType

COMMENT_MAX_LENGTH = getattr(settings, 'COMMENT_MAX_LENGTH', 3000)

class Comment(CommentMixin, models.Model):
    """
    """
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('author'), related_name="%(class)s_comments")

    content_type = models.ForeignKey(ContentType,
            verbose_name=_('content type'),
            related_name="content_type_set_for_%(class)s")
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
        return "%s: %s..." % (self.author.username, self.comment[:50])


class ObjectTask(models.Model):
    """
    """
    task = models.ForeignKey(Task, verbose_name=_('task'), related_name="%(class)s_tasks")

    content_type = models.ForeignKey(ContentType,
            verbose_name=_('content type'),
            related_name="content_type_set_for_%(class)s")
    object_id = models.TextField(_('object ID'))
    content_object = GenericForeignKey()

    class Meta:
        verbose_name = _('objecttask')
        verbose_name_plural = _('objecttasks')

    def __str__(self):
        return "%s for %s" % (str(self.task), str(self.content_object))





def upload_manager(instance, filename):
	user = instance.project.author
	user_profile = Profile.objects.get(user=user)
	user_organisation = user_profile.organisation
	user_project = instance.project.name
	# b = str(MEDIA_ROOT)
	a = user_organisation+'/'+user_project+'/'+filename+'/'
	return a
	# return MEDIA_ROOT

class MediaUpload(models.Model):
	project = models.ForeignKey(Project, related_name='files_project', on_delete=models.CASCADE)
	# owner = models.ForeignKey(User, on_delete=models.CASCADE)
	media = models.FileField(upload_to=upload_manager)
	mimetype = models.CharField(max_length=255, null=True, blank=True)
	file_description = models.TextField()
	hash = models.CharField(max_length=128, db_index=True)
	def __unicode__(self):
		return 'File: %s %s'%(self.media.name, self.mimetype)

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
# 		return str(self.comment)

from follow import utils
from reversion import revisions as reversion

reversion.register(Task)

utils.register(User)

utils.register(Project)
# utils.register(Milestone)
utils.register(Task)

# # IMPORTANT LINE, really leave it there!
# from django_project import handlers
