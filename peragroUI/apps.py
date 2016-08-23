from __future__ import unicode_literals

from django.apps import AppConfig, apps
# from django.contrib.auth.models import User

class PeragrouiConfig(AppConfig):
    name = 'peragroUI'
    def ready(self):
        from actstream import registry
        registry.register(apps.get_model('auth.user'))
        registry.register(self.get_model('UiComment'))
        registry.register(self.get_model('MediaUpload'))
        registry.register(self.get_model('TaskUI'))
        registry.register(self.get_model('Role'))
        
        # registry.register('Profile')