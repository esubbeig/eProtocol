from django.db import models
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.contrib.postgres.fields import CITextField

from ckeditor.fields import RichTextField

from core.models import TherapeuticArea

# eProtocol Templates information
class eProtocolTemplate(models.Model):
    # name = models.CharField(max_length=2048, unique=True, error_messages={'unique':"This name is already existed."})
    # code = models.CharField(max_length=254, blank=True, null=True, unique=True, error_messages={'unique':"This code is already existed."})
    code = models.CharField(max_length=254, blank=True, null=True)
    therapeutic_area= models.ForeignKey(TherapeuticArea, on_delete=models.CASCADE, blank=True, null=True)
    version_no = models.CharField(max_length=10)
    delete = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    has_data = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        db_table = 'eProtocolTemplate'

    @property
    def is_active(self):
        'Is the Protocol Template active?'
        return self.active
    
    @property
    def is_delete(self):
        'Is the Protocol Template deleted?'
        return self.delete


# eProtocol Template sections
class eProtocolTemplateSections(models.Model):
    sec_heading = models.TextField()
    sec_content = models.TextField(blank=True, null=True)
    # sec_content = RichTextField(blank=True, null=True)
    read_only = models.CharField(max_length=10, blank=True, null=True)
    template = models.ForeignKey(eProtocolTemplate, on_delete=models.CASCADE)

    class Meta:
        db_table = 'eProtocolTemplateSections'



# eProtocol Project information
class eProtocolProjectInfo(models.Model):
    code = models.CharField(max_length=254, unique=True, error_messages={'unique':"This code id already existed."})
    name = models.CharField(max_length=1024, unique=True, error_messages={'unique':"This name id already existed."})
    short_name = models.CharField(max_length=1024, null=True, blank=True)
    upin = models.CharField(max_length=30, null=True, blank=True)
    nct = models.CharField(max_length=254, null=True, blank=True)
    study_type = models.CharField(max_length=100, null=True, blank=True)
    funding_entity = models.TextField(null=True, blank=True)
    ind_sponsor = models.CharField(max_length=1024, null=True, blank=True)
    therapeutic_area= models.ForeignKey(TherapeuticArea, on_delete=models.CASCADE)
    sub_speciality = models.CharField(max_length=1024)
    template = models.ForeignKey(eProtocolTemplate, on_delete=models.CASCADE)
    archived = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    delete = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_on  = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    @property
    def is_active(self):
        'Is the eProtocol Project active?'
        return self.active
    
    @property
    def is_delete(self):
        'Is the eProtocol Project deleted?'
        return self.delete

    @property
    def is_archived(self):
        'Is the eProtocol Project archived?'
        return self.archived

# eProtocol Template sections
class eProtocolProjectSections(models.Model):
    sec_heading = models.TextField()
    sec_content = models.TextField()
    read_only = models.CharField(max_length=10, blank=True, null=True)
    eProtocolproject = models.ForeignKey(eProtocolProjectInfo, on_delete=models.CASCADE)

    class Meta:
        db_table = 'eProtocolProjectSections'

    def __str__(self):
        return self.sec_heading


# eProtocol project cross users
class eProtocolProjectXUsers(models.Model):
    eProtocolproject = models.ForeignKey(eProtocolProjectInfo, on_delete=models.CASCADE)
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    active      = models.BooleanField(default=True)
    created_on  = models.DateTimeField(auto_now_add=True)
    created_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='eprotocolprojectxusers_created_by')

    @property
    def is_active(self):
        "Is the project is active?"
        return self.active

    class Meta:
        db_table = 'eProtocolProjectXUsers'

# eProtocol Help
class eProtocolHelp(models.Model):
    sec_heading = models.TextField()
    sec_content = RichTextField(blank=True,null=True)

    class Meta:
        db_table = 'eProtocolHelp'


class RefecenceCount(models.Model):
    eProtocolproject = models.ForeignKey(eProtocolProjectInfo, on_delete=models.CASCADE)
    ref_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'RefecenceCount'