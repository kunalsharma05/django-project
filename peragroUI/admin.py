from django.contrib import admin
from django.utils.translation import ugettext as _

from reversion.admin import VersionAdmin

from peragroUI.models import *


admin.site.register(Profile)
admin.site.register(MediaUpload)
admin.site.register(TaskUI)
admin.site.register(Role)
admin.site.register(UiComment)
admin.site.register(AssignedResource_Relation)
    