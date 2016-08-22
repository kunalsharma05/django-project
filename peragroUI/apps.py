from __future__ import unicode_literals

from django.apps import AppConfig


class PeragrouiConfig(AppConfig):
    name = 'peragroUI'
    def ready(self):
        from actstream import registry
        registry.register(self.get_model('UiComment'))
        registry.register(self.get_model('MediaUpload'))