from __future__ import unicode_literals

from django.apps import AppConfig
# from django.contrib.auth.models import User

class Django_projectConfig(AppConfig):
    name = 'django_project'
    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Project'))
        # registry.register(self.get_model('MediaUpload'))
        # registry.register(self.get_model('TaskUI'))
        # registry.register('User')