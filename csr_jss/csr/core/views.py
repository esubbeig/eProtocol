import json
import os
import logging
import math
import decimal
import traceback
from operator import itemgetter

from django.contrib.auth import login, logout, authenticate, update_session_auth_hash, get_user_model
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, Http404, HttpResponseRedirect
# from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt


from .admin_operations import *
from .user_operations import *
from .models import *
from .forms import *
from .generate_csr import *
from .edit_csr_mapping import *
from audits.audit import *

from eprotocol.models import *

from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.core.mail import EmailMessage, get_connection, EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend
from django.views import View

User = get_user_model()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_NAME = BASE_DIR.split('\\')[-1]

csr_logger = logging.getLogger('csr')
csr_except_logger = logging.getLogger('csr_except')


def release_note(request):
    return render(request, 'releasenote.html')
    

def home(request):

    if request.user.is_authenticated:
        
        if request.user.is_superuser:
            csr_projects = ProjectInfo.objects.all().order_by('-id')
            protocol_projects = eProtocolProjectInfo.objects.filter(active=True, delete=False, archived=False).order_by('-id')
            return render(request, 'admin_home.html', {'csr_projects' : csr_projects, 'protocol_projects' : protocol_projects})
            
        elif request.user.user_role.role == 'Global User':
            csr_projects = get_user_projects(request.user.id).order_by('-id')
            protocol_projects = get_user_eprotocol(request.user.id).order_by('-id')
            return render(request, 'global_user_home.html', {'csr_projects' : csr_projects, 'protocol_projects' : protocol_projects})

        elif request.user.user_role.role == 'CSR User':
            csr_projects = get_user_projects(request.user.id).order_by('-id')
            return render(request, 'csr_user_home.html', {'csr_projects' : csr_projects})

        elif request.user.user_role.role == 'eProtocol User':
            protocol_projects = get_user_eprotocol(request.user.id).order_by('-id')
            return render(request, 'eprotocol_user_home.html', {'protocol_projects' : protocol_projects})
    
        return redirect('home')

    else:
        return redirect('login')


@login_required(login_url='/')
def upload_csr_admin(request):

    data = {}

    therapeutic_area_list = TherapeuticArea.objects.all()

    if request.method == 'POST':

        version          = request.POST['version']
        file_Name        = request.FILES['csr_template_location']
        # therapeutic_area = request.POST['therapeutic_area']

        try:
            form = GlobalCsrUploadForm(request.POST, request.FILES)
        except Exception as e:
            csr_except_logger.critical(str(e) + '\n' + str(traceback.format_exc()))            


        if form.is_valid():

            fr__mt = check_file_content(file_Name)

            if fr__mt == '':
            
                dd = form.save(commit=False)
                dd.created_by = request.user

                try:
                    # obj = CSRTemplate.objects.filter(therapeutic_area=therapeutic_area).latest('id').version_no
                    obj = CSRTemplate.objects.latest('id').version_no
                except CSRTemplate.DoesNotExist:
                    obj = None

                if obj is not None:

                    if version == '0.1':
                        ver, rev = obj.split('.')
                        obj = ver + '.' + str(int(rev) + 1)
                    else:
                        ver, rev = obj.split('.')
                        obj = str(int(ver)+1) + '.' + str(0)

                else:
                    obj = version

                dd.version_no = obj
                dd.save()

                # Deleting premapped data in GlobalMappingTable
                try:
                    GlobalMappingTable.objects.all().delete()
                except Exception as e:
                    csr_except_logger.critical(str(e) + '\n' + str(traceback.format_exc()))


                messages.success(request, "Global CSR has been uploaded successfully!")

                #recording user acivity log
                event = 'CSR Upload'
                record_user_activity_log(
                    event       = event, 
                    actor       = request.user,  
                    session_id  = request.session.session_key
                    )

                data['form_is_valid'] = True
                data['file_data_format'] = ''

            else:
                data['form_is_valid'] = False
                data['file_data_format'] = fr__mt
        else:
            # messages.error(request, "Please Upload .docx file only!")
            data['form_is_valid'] = False
            data['file_data_format'] = ''
    else:
        form = GlobalCsrUploadForm()

    context = {

        'form' : form,
        'therapeutic_area_list' : therapeutic_area_list
    }

    data['html_form'] = render_to_string('upload_global_csr_admin.html', context, request=request)
    return JsonResponse(data)


@login_required(login_url='/')
def upload_protocol_admin(request):

    data = {}

    therapeutic_area_list = TherapeuticArea.objects.all()

    if request.method == 'POST':

        version          = request.POST['version']
        file_Name        = request.FILES['protocol_template_location']
        # therapeutic_area = request.POST['therapeutic_area']

        try:
            form = ProtocolUploadAdminForm(request.POST, request.FILES)
        except Exception as e:
            csr_except_logger.critical(str(e) + '\n' + str(traceback.format_exc()))

        if form.is_valid():

            fr__mt = check_file_content(file_Name)

            if fr__mt == '':
            
                dd = form.save(commit=False)
                dd.created_by = request.user

                try:
                    # obj = ProtocolAdmin.objects.filter(therapeutic_area=therapeutic_area).latest('id').version_no
                    obj = ProtocolAdmin.objects.latest('id').version_no
                except ProtocolAdmin.DoesNotExist:
                    obj = None

                if obj is not None:

                    if version == '0.1':
                        ver, rev = obj.split('.')
                        obj = ver + '.' + str(int(rev) + 1)
                    else:
                        ver, rev = obj.split('.')
                        obj = str(int(ver)+1) + '.' + str(0)

                else:
                    obj = version

                dd.version_no = obj
                dd.save()
                messages.success(request, "Protocol has been uploaded successfully!")

                event = 'Upload Protocol'
                record_user_activity_log(
                    event       = event, 
                    actor       = request.user,  
                    session_id  = request.session.session_key
                    )

                data['form_is_valid'] = True
                data['file_data_format'] = ''

            else:
                data['form_is_valid'] = False
                data['file_data_format'] = fr__mt
        else:
            # messages.error(request, "Please Upload .docx file only!")
            data['form_is_valid'] = False
            data['file_data_format'] = ''
    else:
        form = ProtocolUploadAdminForm()

    context = {

        'form' : form,
        'therapeutic_area_list' : therapeutic_area_list
    }

    data['html_form'] = render_to_string('upload_protocol_admin.html', context, request=request)
    return JsonResponse(data)


@login_required(login_url='/')
def upload_sar_admin(request):

    data = {}

    therapeutic_area_list = TherapeuticArea.objects.all()

    if request.method == 'POST':

        version          = request.POST['version']
        # therapeutic_area = request.POST['therapeutic_area']

        try:
            form = SARUploadAdminForm(request.POST, request.FILES)
        except Exception as e:
            csr_except_logger.critical(str(e) + '\n' + str(traceback.format_exc()))


        if form.is_valid():
            
            dd = form.save(commit=False)
            dd.created_by = request.user

            try:
                # obj = SARAdmin.objects.filter(therapeutic_area=therapeutic_area).latest('id').version_no
                obj = SARAdmin.objects.latest('id').version_no
            except SARAdmin.DoesNotExist:
                obj = None

            if obj is not None:

                if version == '0.1':
                    ver, rev = obj.split('.')
                    obj = ver + '.' + str(int(rev) + 1)
                else:
                    ver, rev = obj.split('.')
                    obj = str(int(ver)+1) + '.' + str(0)

            else:
                obj = version

            dd.version_no = obj
            dd.save()
            messages.success(request, "SAR has been uploaded successfully!")

            event = 'Upload SAR'
            record_user_activity_log(
                event       = event, 
                actor       = request.user,  
                session_id  = request.session.session_key
                )

            data['form_is_valid'] = True
        else:
            # messages.error(request, "Please Upload .docx file only!")
            data['form_is_valid'] = False
    else:
        form = SARUploadAdminForm()

    context = {

        'form' : form,
        'therapeutic_area_list' : therapeutic_area_list
    }

    data['html_form'] = render_to_string('upload_sar_admin.html', context, request=request)
    return JsonResponse(data)



# this handle globaL csr upload functionality
@login_required(login_url='/')
def global_csr_upload(request):

    try:

        therapeutic_area_list = TherapeuticArea.objects.all()
        try:
            csr_doc_latest = CSRTemplate.objects.latest('id')
        except CSRTemplate.DoesNotExist:
            csr_doc_latest = None
        try:
            csr_doc_list = CSRTemplate.objects.order_by('-created_on')[1:]
        except CSRTemplate.DoesNotExist:
            csr_doc_list = None

        try:
            protocol_doc_latest = ProtocolAdmin.objects.latest('id')
        except ProtocolAdmin.DoesNotExist:
            protocol_doc_latest = None
        try:
            protocol_doc_list = ProtocolAdmin.objects.order_by('-created_on')[1:]
        except ProtocolAdmin.DoesNotExist:
            protocol_doc_list = None

        try:
            sar_doc_latest = SARAdmin.objects.latest('id')
        except SARAdmin.DoesNotExist:
            sar_doc_latest = None
        try:
            sar_doc_list = SARAdmin.objects.order_by('-created_on')[1:]
        except SARAdmin.DoesNotExist:
            sar_doc_list = None
            
        context = {
            'csr_doc_latest' : csr_doc_latest,
            'csr_doc_list' : csr_doc_list,
            'protocol_doc_latest' : protocol_doc_latest,
            'protocol_doc_list' : protocol_doc_list,
            'sar_doc_latest' : sar_doc_latest,
            'sar_doc_list' : sar_doc_list
        }
        return render(request, 'global_csr_upload.html', context)

    except Exception as e:
        csr_except_logger.critical(str(e) + '\n' + str(traceback.format_exc()))


#this handle the csr upload operation in each project of user
@login_required(login_url='/')
def csr_upload(request, usr_id, pro_id):

    proj = ProjectInfo.objects.get(pk=pro_id)

    data = {}

    therapeutic_area_list = TherapeuticArea.objects.all()

    if request.method == 'POST':

        version          = request.POST['version']
        file_Name        = request.FILES['csr_template_location']

        try:
            form = CsrUploadForm(request.POST, request.FILES)
        except Exception as e:
            csr_except_logger.critical(str(e) + '\n' + str(traceback.format_exc()))
            
        
        if form.is_valid():

            fr__mt = check_file_content(file_Name)

            if fr__mt == '':

                dd = form.save(commit=False)
                dd.project = proj
                dd.created_by = request.user
                try:
                    # obj = CSRTemplateUser.objects.filter(therapeutic_area=therapeutic_area).latest('id').version_no
                    obj = CSRTemplateUser.objects.filter(project=pro_id).latest('id').version_no
                except CSRTemplateUser.DoesNotExist:
                    obj = None

                if obj is not None:

                    if version == '0.1':
                        ver, rev = obj.split('.')
                        obj = ver + '.' + str(int(rev) + 1)
                    else:
                        ver, rev = obj.split('.')
                        obj = str(int(ver)+1) + '.' + str(0)

                else:
                    obj = version

                dd.version_no = obj
                dd.save()

                # Deleting premapped data in GlobalMappingTable
                try:
                    CustomMappingTable.objects.filter(project=pro_id).delete()
                except Exception as e:
                    csr_except_logger.critical(str(e) + '\n' + str(traceback.format_exc()))

                # Logging activity log
                event = 'Custom CSR Upload'
                record_user_activity_log(
                    event       = event, 
                    actor       = request.user,
                    proj_name   = proj.project_name, 
                    session_id  = request.session.session_key
                    )

                messages.success(request, "Custom CSR has been uploaded successfully!")
                data['form_is_valid'] = True
                data['file_data_format'] = ''

            else:
                data['form_is_valid'] = False
                data['file_data_format'] = fr__mt

        else:
            # messages.error(request, "Please Upload .docx file only!")
            data['form_is_valid'] = False
            data['file_data_format'] = ''
    else:
        form = CsrUploadForm()

    context = {

        'form' : form,
        'therapeutic_area_list' : therapeutic_area_list,
        'proj' : proj
    }
    data['html_form'] = render_to_string('csr_upload.html', context, request=request)
    return JsonResponse(data)



#this handle the protocol upload operation in each project of user
@login_required(login_url='/')
def protocol_file_upload(request, usr_id, pro_id):

    proj = ProjectInfo.objects.get(pk=pro_id)


    data = {}

    therapeutic_area_list = TherapeuticArea.objects.all()

    if request.method == 'POST':

        version          = request.POST['version']
        file_Name        = request.FILES['protocol_document_location']

        try:
            form = ProtocolFileUploadForm(request.POST, request.FILES)
        except Exception as e:
            csr_except_logger.critical(str(e) + '\n' + str(traceback.format_exc()))
        
        if form.is_valid():

            fr__mt = check_file_content(file_Name)

            if fr__mt == '':

                dd = form.save(commit=False)
                dd.project = proj
                dd.created_by = request.user
                try:
                    # obj = ProtocolFileUpload.objects.filter(therapeutic_area=therapeutic_area).latest('id').version_no
                    obj = ProtocolFileUpload.objects.filter(project=pro_id).latest('id').version_no
                except ProtocolFileUpload.DoesNotExist:
                    obj = None

                if obj is not None:

                    if version == '0.1':
                        ver, rev = obj.split('.')
                        obj = ver + '.' + str(int(rev) + 1)
                    else:
                        ver, rev = obj.split('.')
                        obj = str(int(ver)+1) + '.' + str(0)

                else:
                    obj = version

                dd.version_no = obj
                dd.save()
                # Logging activity log
                event = 'Protocol Upload'
                record_user_activity_log(
                    event       = event, 
                    actor       = request.user,
                    proj_name   = proj.project_name, 
                    session_id  = request.session.session_key
                    )

                messages.success(request, "Protocol has been uploaded successfully!")
                data['form_is_valid'] = True
                data['file_data_format'] = ''

            else:
                data['form_is_valid'] = False
                data['file_data_format'] = fr__mt

        else:
            # messages.error(request, "Please Upload .docx file only!")
            data['form_is_valid'] = False
            data['file_data_format'] = ''
    else:
        form = ProtocolFileUploadForm()

    context = {

        'form' : form,
        'therapeutic_area_list' : therapeutic_area_list,
        'proj' : proj
    }
    data['html_form'] = render_to_string('protocol_upload.html', context, request=request)
    return JsonResponse(data)

#this handle the sar upload operation in each project of user
@login_required(login_url='/')
def sar_file_upload(request, usr_id, pro_id):

    proj = ProjectInfo.objects.get(pk=pro_id)

    data = {}

    therapeutic_area_list = TherapeuticArea.objects.all()

    if request.method == 'POST':

        version  = request.POST['version']

        try:
            form = SarFileUploadForm(request.POST, request.FILES)
        except Exception as e:
            csr_except_logger.critical(str(e) + '\n' + str(traceback.format_exc()))


        if form.is_valid():
            dd = form.save(commit=False)
            dd.project = proj
            dd.created_by = request.user
            try:
                # obj = SarFileUpload.objects.filter(therapeutic_area=therapeutic_area).latest('id').version_no
                obj = SarFileUpload.objects.filter(project=pro_id).latest('id').version_no
            except SarFileUpload.DoesNotExist:
                obj = None

            if obj is not None:

                if version == '0.1':
                    ver, rev = obj.split('.')
                    obj = ver + '.' + str(int(rev) + 1)
                else:
                    ver, rev = obj.split('.')
                    obj = str(int(ver)+1) + '.' + str(0)

            else:
                obj = version

            dd.version_no = obj
            dd.save()
            # logging activity log
            event = 'SAR Upload'
            record_user_activity_log(
                event       = event, 
                actor       = request.user,
                proj_name   = proj.project_name, 
                session_id  = request.session.session_key
                )

            messages.success(request, "SAR has been uploaded successfully!")
            data['form_is_valid'] = True

        else:
            # messages.error(request, "Please Upload .docx file only!")
            data['form_is_valid'] = False
    else:
        form = SarFileUploadForm()

    context = {

        'form' : form,
        'therapeutic_area_list' : therapeutic_area_list,
        'proj' : proj
    }
    data['html_form'] = render_to_string('sar_upload.html', context, request=request)
    return JsonResponse(data)


@login_required(login_url='/')
def create_project(request, usr_id):
    
    therapeutic_area_list = TherapeuticArea.objects.all()

    data = {}

    if request.method == 'POST':
        
        try:
            form = CreateProjectForm(request.POST or None)
        except Exception as e:
            csr_except_logger.critical(str(e) + '\n' + str(traceback.format_exc()))


        if form.is_valid():
            dd = form.save(commit=False)
            dd.created_by   = request.user
            dd.save()
            #updating projectsXusers
            projectxusers = ProjectsXUsers(project=dd, user=request.user, created_by=request.user)
            projectxusers.save()
            #updating userprojectcount
            try:
                y = ProjectsXUsers.objects.filter(user=usr_id, active=True).count()
                proj_count = UserProjectCount.objects.get(user=usr_id)
                proj_count.project_count = y
                proj_count.save()
            except:
                pass
            
            messages.success(request, "Project has been created successfully!")
            data['form_is_valid'] = True

            #recording activity log
            event = 'Create Project'
            record_user_activity_log(
                event       = event, 
                actor       = request.user, 
                proj_name   = dd.project_name, 
                session_id  = request.session.session_key
                )

        else:
            data['form_is_valid'] = False
    else:
        form = CreateProjectForm()

    context = {

        'form' : form,
        'therapeutic_area_list' : therapeutic_area_list,
    }
    data['html_form'] = render_to_string('create_project.html', context, request=request)
    return JsonResponse(data)

    

#this will get the project details
@login_required(login_url='/')
def get_projects_admin(request):
    users        = get_all_users()
    project_list = get_all_project_list()
    
    return render(request, 'assign_project.html', {'project_list' : project_list,  'users' : users})



@login_required(login_url='/')
def assign_project_new(request, prj_id):

    pre = []
    post = []

    post_assigned_user_emails = []

    project = ProjectInfo.objects.get(pk=prj_id)

    # recording pre assinged users
    pre_assigned_user_names_active = ProjectsXUsers.objects.filter(project=prj_id, active=True)
    for i in pre_assigned_user_names_active:
        pre.append(i.user.username)

    #to get all the records
    pre_assigned_all = ProjectsXUsers.objects.filter(project=prj_id)
    pre_assigned_user_ids_all = []
    for m in pre_assigned_all:
        pre_assigned_user_ids_all.append(m.user.id)

    #to get all active records which passed into the form
    pre_assigned_active = ProjectsXUsers.objects.filter(project=prj_id, active=True)
    pre_assigned_user_ids_active = []   

    for n in pre_assigned_active:
        pre_assigned_user_ids_active.append(n.user.id)
    
    pre_assigned_user_ids_all = set(pre_assigned_user_ids_all)
    pre_assigned_user_ids_active = set(pre_assigned_user_ids_active)

    data = {}
    
    users = get_all_csr_users_active()

    if request.method == 'POST':
        some_values = request.POST.getlist('check_user')
        if len(some_values) > 0:
            
            for i in range(len(some_values)):
                try:
                    temp = ProjectsXUsers.objects.get(project=prj_id, user=int(some_values[i]))
                    if temp:
                        if temp.is_active:
                            pass
                        else:
                            temp.active = True
                            temp.save()
                except ProjectsXUsers.DoesNotExist:
                    temp = ProjectsXUsers(created_by = User.objects.get(pk=1), project=ProjectInfo.objects.get(pk=prj_id), user=User.objects.get(pk=int(some_values[i])))
                    temp.save()

            #this makes the record deactive if user is unchecked
            new_values = set(int(l) for l in some_values)
            for j in pre_assigned_user_ids_all:
                if j in new_values:
                    pass
                else:
                    try:
                        temp = ProjectsXUsers.objects.get(project=prj_id, user=User.objects.get(pk=j))
                        temp.active = False
                        temp.save()
                    except:
                        pass

            #updating project count table
            for k in users:
                try:
                    upc = UserProjectCount.objects.get(user=k.id)
                    upc.project_count = ProjectsXUsers.objects.filter(user=k.id, active=True).count()
                    upc.save()
                except UserProjectCount.DoesNotExist:
                    pass

            # recording post assinged users
            post_assigned_user_names_active = ProjectsXUsers.objects.filter(project=prj_id, active=True)
            for i in post_assigned_user_names_active:
                post.append(i.user.username)
                post_assigned_user_emails.append(i.user.email)

            # recording audit log
            client_ip = request.META['REMOTE_ADDR']
            assign_project_log(pre, post, request.user, client_ip)

            #recording activity log
            event = 'Assign Project'
            record_user_activity_log(
                event       = event, 
                actor       = request.user, 
                proj_name   = project.project_name, 
                session_id  = request.session.session_key
                )

            #to send alert email
            try:
                config  = EmailConfiguration.objects.last()
            except EmailConfiguration.DoesNotExist:
                config = None
            
            backend = EmailBackend(

                host          = config.email_host,
                username      = config.email_host_user,
                password      = config.email_host_password,
                port          = config.email_port,
                use_tls       = True,
                fail_silently = True

            )
            from_email = config.email_default_mail
            current_site = get_current_site(request)
            email_subject = 'Project Assignement in CSR.'
            
            for i in range(len(post)):
                if post_assigned_user_emails[i] != '':

                    to_email = post_assigned_user_emails[i]
                    html_content = "<h3>Dear <b>"+ post[i] +"</b>,</h3><br>You have been assinged with a new project, <b>" + project.project_name + "</b><br><br><b>Thanks & Regards<br>CSR Automation</b>"

                    email = EmailMessage(subject=email_subject, body=html_content, from_email=from_email, to=[to_email], connection=backend)
                    email.content_subtype = 'html'
                    email_status = email.send()
            
                    # recording Email logs
                    e_log = LogsEmails(

                            event = 'Assign Project',
                            to_email = to_email,
                            from_email = from_email,
                            subject = email_subject,
                            message_body = html_content,
                            email_sent = email_status,
                            created_by = request.user

                        )
                    e_log.save()         

            messages.success(request, "Project has been Assigned successfully!")
            data['form_is_valid'] = True
        else:
            data['form_is_valid'] = False

    context = {

        'users' : users,
        'project' : project,
        'pre_assigned_user_ids_active' : pre_assigned_user_ids_active

    }

    data['html_form'] =  render_to_string('assign_project.html', context, request=request)
    return JsonResponse(data)



#this fetches all the users project details
@login_required(login_url='/')
def get_all_users_details(request):

    try:
        config = EmailConfiguration.objects.last()
    except EmailConfiguration.DoesNotExist:
        config = None
    
    proj_count = UserProjectCount.objects.all()
    users = get_all_users_active()
    return render(request, 'admin_users.html', {'users' : users,  'proj_count' : proj_count, 'config' : config})


#this fetches all the users project details
@login_required(login_url='/')
def get_all_active_users_details(request):

    data = {}

    try:
        config = EmailConfiguration.objects.last()
    except EmailConfiguration.DoesNotExist:
        config = None
    
    proj_count = UserProjectCount.objects.all()
    users = get_all_users_active()
    context ={
        'users'      : users,
        'proj_count' : proj_count,
        'config'     : config
    }
    data['html_form'] =  render_to_string('admin_users_partial.html', context, request=request)
    return JsonResponse(data)


#this fetches all the users project details
@login_required(login_url='/')
def get_all_act_inact_users_details(request):

    data = {}

    try:
        config = EmailConfiguration.objects.last()
    except EmailConfiguration.DoesNotExist:
        config = None
    
    proj_count = UserProjectCount.objects.all()
    users = get_all_users()
    context ={
        'users'      : users,
        'proj_count' : proj_count,
        'config'     : config
    }
    data['html_form'] =  render_to_string('admin_users_partial.html', context, request=request)
    return JsonResponse(data)


@login_required(login_url='/')
def edit_user_project(request, usr_id, proj_id):

    projects = ProjectInfo.objects.get(pk=proj_id)
    therapeutic_area_list = TherapeuticArea.objects.all()

    data = {}

    if request.method == 'POST':
        form = EditProjectForm(request.POST or None, instance=projects)
        if form.is_valid():

            # recording previous state
            previoust_state = ProjectInfo.objects.get(pk=proj_id)

            # updating project details
            projects.project_name     = request.POST.get('project_name')
            projects.protocol_id      = request.POST.get('protocol_id')
            projects.client           = request.POST.get('client')
            projects.therapeutic_area = TherapeuticArea.objects.get(pk=request.POST.get('therapeutic_area'))
            projects.phase            = request.POST.get('phase')
            projects.save()

            # recording current state
            current_state = ProjectInfo.objects.get(pk=proj_id)

            # recording audit log
            client_ip = request.META['REMOTE_ADDR']
            edit_project_log(previoust_state, current_state, projects, request.user, client_ip)

            #recording activity log
            event = 'Edit Project'
            record_user_activity_log(
                event       = event, 
                actor       = request.user,
                proj_name   = request.POST.get('project_name'),
                session_id  = request.session.session_key
                )

            messages.success(request, "Project " + current_state.project_name + " has been updated successfully!")
            data['form_is_valid'] = True

        else:
            data['form_is_valid'] = False

    else:
        form = EditProjectForm()

    context = {

        'form' : form,
        'projects' : projects,
        'therapeutic_area_list' : therapeutic_area_list

    }
    data['html_form'] =  render_to_string('edit_user_project.html', context, request=request)
    return JsonResponse(data)



#each project dashboard
@login_required(login_url='/')
def project_dashboard(request, usr_id, proj_id):

    projects = ProjectInfo.objects.get(pk=proj_id)

    # Latest Global CSR
    try:
        csr_doc_latest = CSRTemplate.objects.latest('id')
    except CSRTemplate.DoesNotExist:
        csr_doc_latest = None
    # List of Global CSR
    try:
        csr_doc_list = CSRTemplate.objects.order_by('-created_on')[1:]
    except CSRTemplate.DoesNotExist:
        csr_doc_list = None

    # Latest Custom CSR
    try:
        custom_csr_doc_latest = CSRTemplateUser.objects.filter(project=proj_id).latest('id')
    except CSRTemplateUser.DoesNotExist:
        custom_csr_doc_latest = None
    # List of Custom CSR
    try:
        custom_csr_doc_list = CSRTemplateUser.objects.filter(project=proj_id).order_by('-created_on')[1:]
    except CSRTemplateUser.DoesNotExist:
        custom_csr_doc_list = None


    # Latest Protocol
    try:
        protocol_doc_latest = ProtocolFileUpload.objects.filter(project=proj_id).latest('id')
    except ProtocolFileUpload.DoesNotExist:
        protocol_doc_latest = None
    # List of Protocol
    try:
        protocol_doc_list = ProtocolFileUpload.objects.filter(project=proj_id).order_by('-uploaded_on')[1:]
    except ProtocolFileUpload.DoesNotExist:
        protocol_doc_list = None


    # Latest SAR
    try:
        sar_doc_latest = SarFileUpload.objects.filter(project=proj_id).latest('id')
    except SarFileUpload.DoesNotExist:
        sar_doc_latest = None
    # List of SAR
    try:
        sar_doc_list = SarFileUpload.objects.filter(project=proj_id).order_by('-uploaded_on')[1:]
    except SarFileUpload.DoesNotExist:
        sar_doc_list = None

    # Latest CSR Report
    try:
        csr_report_latest = Generated_Reports.objects.filter(project=proj_id).latest('id')
    except Generated_Reports.DoesNotExist:
        csr_report_latest = None
    # List of CSR Report
    try:
        csr_report_list = Generated_Reports.objects.filter(project=proj_id).order_by('-created_on')[1:]
    except Generated_Reports.DoesNotExist:
        csr_report_list = None


    context = {

        'projects'            : projects,
        'csr_doc_latest'      : csr_doc_latest,
        'csr_doc_list'        : csr_doc_list,
        'custom_csr_doc_latest' : custom_csr_doc_latest,
        'custom_csr_doc_list' : custom_csr_doc_list,
        'protocol_doc_latest' : protocol_doc_latest,
        'protocol_doc_list'   : protocol_doc_list,
        'sar_doc_latest'      : sar_doc_latest,
        'sar_doc_list'        : sar_doc_list,
        'csr_report_latest'   : csr_report_latest,
        'csr_report_list'     : csr_report_list,
        'usr_id'              : usr_id

    }

    return render(request, 'project_dashboard.html', context)




#to download any file
@login_required(login_url='/')
def download(request, path):
    
    file_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(file_path):

        with open(file_path, 'rb') as fh:

            response = HttpResponse(fh.read(), content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)

            return response

    raise Http404

# to handle activity log
@login_required(login_url='/')
def activity_log(request, usr_id):

    data  = {}

    users = get_all_users()
    
    logs = LogsActivity.objects.filter(userid=usr_id)

    if logs:
        logs  = LogsActivity.objects.filter(userid=usr_id).order_by('-id')

    return render(request, 'activity_log.html', {'logs' : logs, 'users' : users})


# to handle activity log on change event in admin
@login_required(login_url='/')
def activity_log_on_change(request, usr_id):

    data  = {}

    logs = LogsActivity.objects.filter(userid=usr_id)

    if logs:
        logs  = LogsActivity.objects.filter(userid=usr_id).order_by('-id')

    username = User.objects.get(pk=usr_id).username

    context = {
        'logs' : logs,
        
    }
    data['username'] = username
    data['html_form'] = render_to_string('activity_log_partial.html', context, request=request)
    return JsonResponse(data)


# to handle audit log
@login_required(login_url='/')
def audit_log(request, usr_id):

    users = get_all_users()

    user = User.objects.get(pk=usr_id)

    if user.is_superuser:
       audit_logs = AuditLogsForMappingAdmin.objects.filter(user=usr_id).order_by('-id')

    else:
        audit_logs = AuditLogsForMappingUser.objects.filter(user=usr_id).order_by('-id')

    return render(request, 'audit_log.html', {'audit_logs' : audit_logs, 'users' : users})


# to handle audit log on change event in admin
@login_required(login_url='/')
def audit_log_on_change(request, usr_id):

    data  = {}

    user = User.objects.get(pk=usr_id)

    if user.is_superuser:
       audit_logs = AuditLogsForMappingAdmin.objects.filter(user=usr_id).order_by('-id')

    else:
        audit_logs = AuditLogsForMappingUser.objects.filter(user=usr_id).order_by('-id')

    username = user.username

    context = {
        'audit_logs' : audit_logs,
        'user' : user
    }
    data['username'] = username
    data['html_form'] = render_to_string('audit_log_partial.html', context, request=request)
    return JsonResponse(data)


# to dispaly global mapping in users role
@login_required(login_url='/')
def display_global_csr_mapping(request):

    mapping_table = list(GlobalMappingTable.objects.all())

    ch_cnt = global_mapping_table_structure(mapping_table)

    context       = {

        'mapping_table' : mapping_table,
        'ch_cnt' : ch_cnt

    }

    return render(request, 'global_csr_mapping.html', context=context)


@login_required(login_url='/')
@csrf_exempt
def generate_csr(request, usr_id, proj_id):

    data = {}
    filename = ''
    version  = ''

    if request.is_ajax():

        response_data = json.loads(request.body)
        filename = response_data[0]
        version = response_data[1]

    projects = ProjectInfo.objects.get(pk=proj_id)
    # recording logging
    csr_logger.info("Generate CSR started for project - '" + projects.project_name +"' by - " + request.user.username)

    status = generate_csr_document(usr_id, proj_id, filename, version)

    if status == 1:
        # to update project info if csr generated
        obj = ProjectInfo.objects.get(pk=proj_id)
        obj.generated = True
        obj.save()

        # messages.success(request, "CSR generated scuccessfully!")

        # recording activity log
        event = 'Generate CSR'
        record_user_activity_log(
            event       = event, 
            actor       = request.user,
            proj_name   = projects.project_name,
            session_id  = request.session.session_key
            )

        messages.success(request, "CSR generated succesfully!")
        data['form_is_valid'] = True
        # recording logging
        csr_logger.info("Generate CSR completed for project - '" + projects.project_name +"' by - " + request.user.username)

    elif status == 2:
        messages.info(request, "CSR generated succesfully! But Some sections of data is not Copied, due to invalid format.")
        data['form_is_valid'] = True

    else:
        messages.error(request, "Custom Mapping not found. Please map through Edit Mapping!")
        data['form_is_valid'] = False

    return JsonResponse(data)



@login_required(login_url='/')
def search_user_project(request):

    query = request.GET.get('search_user_project')

    results = ProjectsXUsers.objects.filter(Q(project__project_name__icontains=query) | Q(project__protocol_id__icontains=query) | Q(project__therapeutic_area__therapeutic_area__icontains=query), user=request.user, active=True)

    data = {

        'results' : results

    }
    return render(request, 'search_user_project.html', {'results' : results})


@login_required(login_url='/')
def search_admin_project(request):

    query = request.GET.get('search_admin_project')

    results = ProjectInfo.objects.filter(Q(project_name__icontains=query) | Q(protocol_id__icontains=query) | Q(therapeutic_area__therapeutic_area__icontains=query), active=True)

    data = {

        'results' : results

    }
    return render(request, 'search_admin_project.html', {'results' : results})


    
from operator import itemgetter
# edit csr mapping user
@csrf_exempt
def edit_csr_mapping(request, usr_id, proj_id):

    projects = ProjectInfo.objects.get(pk=proj_id)

    fetched_data      = get_global_mapped_data_usr(usr_id, proj_id)
    custom_mapping    = fetched_data[0]
    csr_headings      = fetched_data[1]
    protocol_headings = fetched_data[2]
    sar_headings      = fetched_data[3]

    # global admin mapped data
    # global_pre_mapped_headings = get_global_mapped_data()
    pre_global_mapping = get_global_mapping_suggestions(csr_headings, protocol_headings, sar_headings)

    global_pre_mapped_headings = pre_global_mapping[0]
    list_global_pre_mapped_csr_headings = list(map(itemgetter('csr_heading'), global_pre_mapped_headings))

    global_pre_mapped_headings_parent = pre_global_mapping[1]
    list_global_pre_mapped_csr_headings_parent = list(map(itemgetter('csr_heading'), global_pre_mapped_headings_parent))
    # print(list_global_pre_mapped_csr_headings)

    record_len = len(csr_headings) + len(global_pre_mapped_headings)

    loop = len(custom_mapping)

    if request.method == 'POST':
        
        csr_headings_data  = request.POST.getlist('csr_headings[]')
        source_data        = request.POST.getlist('source[]')
        copy_headings_data = request.POST.getlist('copy_headings[]')
        reason             = request.POST.get('reason')
        parent_ids         = request.POST.getlist('child_parent_id[]')

        status = load_custom_mapping_to_model(csr_headings_data, source_data, copy_headings_data,usr_id, proj_id, parent_ids)

        if status == 1:
            messages.success(request, 'Custom Mapping table updated scuccessfully!')

            # recording audit log
            client_ip = request.META['REMOTE_ADDR']
            edit_custom_csr_mapping_log(custom_mapping, csr_headings_data, source_data, copy_headings_data, reason, request.user, projects, client_ip)

            # recording activity log
            event = 'Edit Custom CSR'
            record_user_activity_log(
                event       = event, 
                actor       = request.user,
                proj_name   = projects.project_name, 
                session_id  = request.session.session_key
                )

            return redirect('project_dashboard', usr_id=usr_id, proj_id=proj_id)
            
        else:
            messages.error(request, 'Please Map again!')


    context = {
        'projects'          : projects,
        'loop'              : loop,
        'custom_mapping'    : custom_mapping,
        'csr_headings'      : csr_headings,
        'protocol_headings' : protocol_headings,
        'sar_headings'      : sar_headings,
        'proj_id'           : proj_id,
        'usr_id'            : usr_id,
        'global_pre_mapped_headings' : global_pre_mapped_headings,
        'list_global_pre_mapped_csr_headings' : list_global_pre_mapped_csr_headings,
        'global_pre_mapped_headings_parent' : global_pre_mapped_headings_parent,
        'list_global_pre_mapped_csr_headings_parent' : list_global_pre_mapped_csr_headings_parent,
        'record_len' : record_len,

    }
    

    return render(request, 'edit_mapping.html', context)


# csr mapping confirmation user
@csrf_exempt
def confirm_csr_mapping_user(request, usr_id, proj_id):
    
    data = {}

    # fetched_data = get_global_mapped_data_usr(usr_id, proj_id)
    # custom_mapping = fetched_data[0]
    custom_mapping = filtered_pre_mapped_user_data(usr_id, proj_id)

    csr_head = ''
    src_file = ''
    src_head = ''
    parent_ids = ''

    if request.is_ajax():
        response_data = json.loads(request.body)
        csr_head = response_data[0]
        src_file = response_data[1]
        src_head = response_data[2]
        parent_ids = response_data[3]

    updated_mapping_form_data = csr_updated_user_form_data(csr_head, src_file, src_head, parent_ids)

    context = {
        'updated_mapping_form_data' : updated_mapping_form_data,
        'custom_mapping' : custom_mapping
    }
    # print(type(custom_mapping))

    data['html_form'] = render_to_string('confirm_csr_mapping_user.html', context, request=request)
    return JsonResponse(data)



# Admin csr mapping
from .admin_csr_mapping import *
def csr_mapping(request):
    
    file_locations      = get_file_locations()
    csr_headings        = GetHeadings_addHeaderNumbering(file_locations[0])
    protocol_headings   = GetHeadings_addHeaderNumbering(file_locations[1])
    sar_headings        = get_all_headings(file_locations[2])
    pre_mapped_headings = get_global_mapped_data()

    try:
        protocol_headings_json = json.dumps(protocol_headings)
        sar_headings_json      = json.dumps(sar_headings)
    except Exception as e:
        csr_except_logger.critical(str(e) + '\n' + str(traceback.format_exc()))


    if request.method == 'POST':
        
        csr_headings_data  = request.POST.getlist('csr_headings[]')
        source_data        = request.POST.getlist('source[]')
        copy_headings_data = request.POST.getlist('copy_headings[]')
        reason             = request.POST.get('reason')
        parent_ids         = request.POST.getlist('child_parent_id[]')

        status = load_mapping_to_model(csr_headings_data, source_data, copy_headings_data, parent_ids)

        if status == 1:
            messages.success(request, 'Global Mapping table updated scuccessfully!')

            # recording audit log
            client_ip = request.META['REMOTE_ADDR']
            edit_global_csr_mapping_log(pre_mapped_headings, csr_headings_data, source_data, copy_headings_data, reason, request.user, client_ip)

            # recording activity log
            event = 'CSR Mapping'
            record_user_activity_log(
                event       = event, 
                actor       = request.user,  
                session_id  = request.session.session_key
                )

            return redirect('global_csr_upload')

        else:
            messages.error(request, 'Please Map again!')

    context = {

        'csr_headings'        : csr_headings,
        'protocol_headings'   : protocol_headings,
        'protocol_headings_json' : protocol_headings_json,
        'sar_headings'        : sar_headings,
        'sar_headings_json'      : sar_headings_json,
        'pre_mapped_headings' : pre_mapped_headings
    }
    
    return render(request, 'admin_csr_mapping.html', context)


# csr mapping confirmation admin
@csrf_exempt
def confirm_csr_mapping_admin(request):
    
    data = {}

    pre_mapped_headings = filtered_pre_mapped_admin_data()

    csr_head = ''
    src_file = ''
    src_head = ''
    parent_ids = ''

    if request.is_ajax():

        response_data = json.loads(request.body)
        csr_head = response_data[0]
        src_file = response_data[1]
        src_head = response_data[2]
        parent_ids = response_data[3]

    updated_mapping_form_data = csr_updated_admin_form_data(csr_head, src_file, src_head, parent_ids, pre_mapped_headings)

    context = {
        'updated_mapping_form_data' : updated_mapping_form_data,
        'pre_mapped_headings' : pre_mapped_headings
    }
    

    data['html_form'] = render_to_string('confirm_csr_mapping_admin.html', context, request=request)
    return JsonResponse(data)


# Handles Chained dropdown for admin protocol mapping
def ad_on_change_protocol_headings(request):

    data = {}

    file_locations = get_file_locations()
    protocol_headings = get_all_headings(file_locations[1])

    context = {
        'protocol_headings' : protocol_headings
    }
    data['html_form'] = render_to_string('ad_protocol_headings.html', context, request=request)

    return JsonResponse(data)
    

# Handles Chained dropdown for admin sar mapping
def ad_on_change_sar_headings(request):

    data = {}

    file_locations = get_file_locations()
    sar_headings = get_all_headings(file_locations[2])
    
    context = {
        'sar_headings' : sar_headings
    }
    data['html_form'] = render_to_string('ad_sar_headings.html', context, request=request)
    
    return JsonResponse(data)


# Handles Chained dropdown for user protocol mapping
def usr_on_change_protocol_headings(request, p_id):

    data = {}

    user_id = request.user.id
    project_id = ProjectInfo.objects.get(pk=p_id).id

    fetched_data      = get_global_mapped_data_usr(user_id, project_id)

    protocol_headings = fetched_data[2]

    context = {
        'protocol_headings' : protocol_headings
    }
    data['html_form'] = render_to_string('usr_protocol_headings.html', context, request=request)

    return JsonResponse(data)
    

# Handles Chained dropdown for user sar mapping
def usr_on_change_sar_headings(request, p_id):

    data = {}

    user_id = request.user.id
    project_id = ProjectInfo.objects.get(pk=p_id).id

    fetched_data = get_global_mapped_data_usr(user_id, project_id)
    sar_headings = fetched_data[3]
    
    context = {
        'sar_headings' : sar_headings
    }
    data['html_form'] = render_to_string('usr_sar_headings.html', context, request=request)
    
    return JsonResponse(data)

# fetches the csr headings in admin edit csr section
def ad_csr_headings(request):

    data = {}

    file_locations = get_file_locations()
    csr_headings = get_all_headings(file_locations[0])

    context = {
        'csr_headings' : csr_headings
    }
    data['html_form'] = render_to_string('ad_csr_headings.html', context, request=request)

    return JsonResponse(data)

# fetches the custom csr headings in user edit csr section
def usr_csr_headings(request, p_id):

    data = {}

    user_id = request.user.id
    project_id = ProjectInfo.objects.get(pk=p_id).id

    fetched_data = get_global_mapped_data_usr(user_id, project_id)
    custom_csr_headings = fetched_data[1]
    
    context = {
        'custom_csr_headings' : custom_csr_headings
    }
    data['html_form'] = render_to_string('custom_csr_headings.html', context, request=request)
    
    return JsonResponse(data)
    

def email_configuration(request):

    data = {}

    if request.method == 'POST':
        form = EmailConfigurationForm(request.POST)
        if form.is_valid():

            # to delete already existed records
            EmailConfiguration.objects.all().delete()

            config = form.save(commit=False)
            config.created_by = request.user
            config.save()
            
            data['form_is_valid'] = True
            messages.success(request, 'Email Configuration added succesfully')

        else:
            data['form_is_valid'] = False
    else:
        form = EmailConfigurationForm()
        
    context = {
        'form' : form
    }
    data['html_form'] = render_to_string('email_configuration.html', context, request=request)
    return JsonResponse(data)

@login_required
def mail_logs(request):

    data = {}

    if request.user.is_superuser:

        try:
            email_logs = LogsEmails.objects.all().order_by('-id')

        except LogsEmails.DoesNotExist:

            email_logs = None

        context = {

            'email_logs' : email_logs,
        }

        return render(request, 'mail_logs.html', context)

@login_required
def resend_email(request, mail_id):

    data = {}

    obj = LogsEmails.objects.get(pk=mail_id)

    #to resend email
    config  = EmailConfiguration.objects.last()
    backend = EmailBackend(

        host          = config.email_host,
        username      = config.email_host_user,
        password      = config.email_host_password,
        port          = config.email_port,
        use_tls       = True,
        fail_silently = True

    )
    from_email = config.email_default_mail
    email_subject = obj.subject
    to_email = obj.to_email
    html_content = obj.message_body
    email = EmailMessage(subject=email_subject, body=html_content, from_email=from_email, to=[to_email], connection=backend)
    email.content_subtype = 'html'
    email_status = email.send()

    # recording Email logs
    e_log = LogsEmails(

            event = obj.event,
            to_email = to_email,
            from_email = from_email,
            subject = email_subject,
            message_body = html_content,
            email_sent = email_status,
            created_by = request.user

        )
    if email_status:

        obj.email_sent = True
        obj.save()

        e_log.email_response = "Email sent scuccessfully"
        data['resend_status'] = True

        messages.success(request, 'Resend Email succesfully!')

        #recording activity log
        event = 'Resend Email'
        record_user_activity_log(
            event       = event,
            actor       = request.user, 
            email       = to_email,
            log_event   = obj.event, 
            session_id  = request.session.session_key
            )

    else:
        e_log.email_response = "Not able to connect SMTP server"
        data['resend_status'] = False
        messages.error(request, 'Problem with connecting SMTP server. Please check the Email Configurations!')

    e_log.save()

    return JsonResponse(data)


@login_required
def display_logging(request):
    log_arr = []

    file = BASE_DIR+'\\'+'media'+'\\logs\\'+'error.log'

    with open(file) as f:
        lines = f.read()
        temp = []
        spl_lines = lines.split('\n[')

        log_arr = spl_lines[::-1]

    return render(request, 'logging.html', {'log_arr' : log_arr})
    