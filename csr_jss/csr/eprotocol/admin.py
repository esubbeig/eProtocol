from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

admin.site.register(eProtocolTemplate)

admin.site.register(eProtocolProjectInfo)

admin.site.register(eProtocolProjectSections)


@admin.register(eProtocolTemplateSections)
class eProtocolTemplateSectionsAdmin(ImportExportModelAdmin):
    pass

@admin.register(eProtocolHelp)
class eProtocolHelpAdmin(ImportExportModelAdmin):
    pass

    
