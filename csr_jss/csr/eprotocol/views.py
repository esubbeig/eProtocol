import json
import pandas as pd

from metapub import PubMedFetcher

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from django.core.mail import EmailMessage, get_connection, EmailMultiAlternatives
from django.core.mail.backends.smtp import EmailBackend

from core.models import *
from core.admin_operations import *

from .forms import *
from .models import *
from .eprotocol_admin_operations import *
from audits.audit import *
from .generate_protocol import GenerateProtocol

# This will render the Protocol Templates page
@login_required(login_url='/')
def ManageProtocolTemplate(request):

    templates_list = eProtocolTemplate.objects.filter(active=True, delete=False).order_by('-id')

    context = {
        'templates_list' : templates_list
    }

    return render(request, 'manage_protocol_template.html', context)



# This view will import the section from csv/excel documents to the templates
@csrf_exempt
@login_required(login_url='/')
def AddContentToTemplate(request, templt_id):

    data = {}

    if request.method == 'POST':

        form = TemplateContentFileForm(request.POST, request.FILES)

        if form.is_valid():

            status = ImportContentToModel(request, request.FILES['file'], templt_id)

            if status == 1:

                data['form_is_valid'] = True
                messages.success(request, "Template content imported successfully!")

        else:
            data['form_is_valid'] = False

    else:
        form = TemplateContentFileForm()

    context = {
        'form' : form,
        'templt_id' : templt_id,
    }

    data['html_form'] = render_to_string('import_template_content.html', context, request=request)
    return JsonResponse(data)


# To view template sections
@login_required(login_url='/')
def ViewTemplateSection(request, templt_id):

    template = eProtocolTemplate.objects.get(pk=templt_id)

    template_sections = eProtocolTemplateSections.objects.filter(template=templt_id).order_by('id')

    context = {
        'template' : template,
        'template_sections' : template_sections,
    }

    return render(request, 'protocol_template_sections.html', context)


# This will hanlde the updating section content
@login_required(login_url='/')
def EditTemplateSection(request, sec_id):

    data = {}

    if request.method == 'POST':

        section = eProtocolTemplateSections.objects.get(pk=sec_id)

        section.sec_content = request.POST.get('sec_content')

        section.save()

        data['form_is_valid'] = True

        messages.success(request, "Record updated successfully!")

    else:
        data['form_is_valid'] = False

    return JsonResponse(data)


# To create a new eProtocol Template
@login_required(login_url='/')
def CreateProtocolTemplate(request):

    data = {}

    therapeutic_area_list = TherapeuticArea.objects.all()

    if request.method == 'POST':

        form = CreateProtocolTemplateForm(request.POST, request.FILES)

        if form.is_valid():

            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.version_no = '0.001'
            obj.save()

            messages.success(request, "Template added successfully!")

            data['form_is_valid'] = True

        else:
            data['form_is_valid'] = False

    else:
        form = CreateProtocolTemplateForm()

    context = {
        'form' : form,
        'therapeutic_area_list' : therapeutic_area_list,
    }
    data['html_form'] = render_to_string('create_protocol_template.html', context, request=request)
    return  JsonResponse(data)


# This will handle eProtocol Template deletion
@csrf_exempt
@login_required(login_url='/')
def DeleteTemplate(request, templt_id):

    data = {}

    if request.method == 'POST':

        try:
            template = eProtocolTemplate.objects.get(pk=templt_id)
        except eProtocolTemplate.DoesNotExist:
            template = None

        if template:

            template.delete = True
            template.save()
            
            messages.success(request, template.code + " deleted successfully!")

    context = {
        'templt_id' : templt_id,
    }

    data['html_form'] = render_to_string('confirm_temp_delete.html', context, request=request)

    return JsonResponse(data)


# This view will handle eProtocol Project creation
@login_required(login_url='/')
def CreateProtocol(request, usr_id):

    data = {}

    therapeutic_area_list = TherapeuticArea.objects.all()

    templates = eProtocolTemplate.objects.filter(active=True, delete=False, has_data=True)

    if request.method == 'POST' and request.is_ajax():

        form = CreateProtocolForm(request.POST)

        if form.is_valid():

            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()

            # Copying section as per template selected
            template_obj_df = pd.DataFrame(list(eProtocolTemplateSections.objects.filter(template=obj.template).values('sec_heading','sec_content','read_only')))

            status = CopyTemplateContentToeProtocolModel(template_obj_df, obj)

            if status == 1:
                data['form_is_valid'] = True
                messages.success(request, "eProtocol created successfully!")

        else:
            data['form_is_valid'] = False

    else:
        form = CreateProtocolForm()

    context = {
        'form' : form,
        'therapeutic_area_list' : therapeutic_area_list,
        'templates' : templates,
    }
    data['html_form'] = render_to_string('create_eprotocol.html', context, request=request)
    return JsonResponse(data)


# This will hanlde the eProtocol Poject updation
@login_required(login_url='/')
def EditeProtocol(request, prot_id):

    data = {}

    protocol = eProtocolProjectInfo.objects.get(pk=prot_id)

    therapeutic_area_list = TherapeuticArea.objects.all()

    templates = eProtocolTemplate.objects.filter(active=True, delete=False, has_data=True)

    if request.method == 'POST':

        form = EditeProtocolForm(request.POST or None, instance=protocol)

        if form.is_valid():

            # recording previous state
            previoust_state = eProtocolProjectInfo.objects.get(pk=prot_id)

            protocol.code = request.POST.get('code')
            protocol.name = request.POST.get('name')
            protocol.short_name = request.POST.get('short_name')
            protocol.therapeutic_area = TherapeuticArea.objects.get(pk=request.POST.get('therapeutic_area'))
            protocol.sub_speciality = request.POST.get('sub_speciality')
            protocol.save()

            # recording current state
            current_state = eProtocolProjectInfo.objects.get(pk=prot_id)

            # recording audit log
            client_ip = request.META['REMOTE_ADDR']
            Edit_eProtocol_Log(previoust_state, current_state, protocol, request.user, client_ip)

            data['form_is_valid'] = True
            messages.success(request, "eProtocol updated successfully!")

        else:
            data['form_is_valid'] = False

    else:
        form = EditeProtocolForm()

    context = {
        'form' : form,
        'therapeutic_area_list' : therapeutic_area_list,
        'templates' : templates,
        'protocol' : protocol,
    }
    data['html_form'] = render_to_string('update_eprotocol.html', context, request=request)
    return JsonResponse(data)


# This view will handle the eProtocol project cloning
@login_required(login_url='/')
def CloneProtocol(request, prot_id):

    data = {}

    therapeutic_area_list = TherapeuticArea.objects.all()

    protocol = eProtocolProjectInfo.objects.get(pk=prot_id)

    if request.method == 'POST':

        form = CloneProtocolForm(request.POST or None)

        if form.is_valid():

            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.therapeutic_area = protocol.therapeutic_area
            obj.sub_speciality = protocol.sub_speciality
            obj.template = protocol.template
            obj.save()

            # Copying section as per template selected
            protocol_obj_df = pd.DataFrame(list(eProtocolProjectSections.objects.filter(eProtocolproject=protocol).values('sec_heading','sec_content','read_only')))

            status = CloneProtocolContent(protocol_obj_df, obj)

            if status == 1:
                data['form_is_valid'] = True
                messages.success(request, "eProtocol cloned successfully!")

        else:
            data['form_is_valid'] = False

    else:
        form = CloneProtocolForm()
        

    context = {
        'form' : form,
        'therapeutic_area_list' : therapeutic_area_list,
        'prot_id' : prot_id,
    }

    data['html_form'] = render_to_string('clone_eprotocol.html', context, request=request)
    return JsonResponse(data)


# This view will handle Archive eProtocol Project
@csrf_exempt
@login_required(login_url='/')
def ArchiveProtocol(request, prot_id):

    data = {}

    if request.method == 'POST':

        try:
            eProtocol = eProtocolProjectInfo.objects.get(pk=prot_id)
        except eProtocolProjectInfo.DoesNotExist:
            eProtocol = None

        if eProtocol:

            eProtocol.archived = True
            eProtocol.save()
            
            messages.success(request, eProtocol.name + " archived successfully!")

    context = {
        'prot_id' : prot_id,
    }

    data['html_form'] = render_to_string('confirm_archive.html', context, request=request)

    return JsonResponse(data)

# This will handle Unarchive eProtocol Project
@login_required(login_url='/')
def UnarchiveProtocol(request, prot_id):

    data = {}

    try:
        eProtocol = eProtocolProjectInfo.objects.get(pk=prot_id)
    except eProtocolProjectInfo.DoesNotExist:
        eProtocol = None

    if request.method == 'POST':

        if eProtocol:

            eProtocol.archived = False
            eProtocol.save()
            
            messages.success(request, eProtocol.name + " unarchived successfully!")

    context = {
        'eProtocol' : eProtocol,
    }

    data['html_form'] = render_to_string('confirm_archive.html', context, request=request)


    return JsonResponse(data)


# This view will hanlde the eProtocol Project assigment to the users
@login_required(login_url='/')
def AssigneProtocolProject(request, prot_id):

    data = {}

    pre = []
    post = []

    post_assigned_user_emails = []

    # recording pre assinged users
    pre_assigned_user_names_active = eProtocolProjectXUsers.objects.filter(eProtocolproject=prot_id, active=True)
    for i in pre_assigned_user_names_active:
        pre.append(i.user.username)

    #to get all the records
    pre_assigned_all = eProtocolProjectXUsers.objects.filter(eProtocolproject=prot_id)
    pre_assigned_user_ids_all = []
    for m in pre_assigned_all:
        pre_assigned_user_ids_all.append(m.user.id)

    #to get all active records which passed into the form
    pre_assigned_active = eProtocolProjectXUsers.objects.filter(eProtocolproject=prot_id, active=True)
    pre_assigned_user_ids_active = []   

    for n in pre_assigned_active:
        pre_assigned_user_ids_active.append(n.user.id)
    
    pre_assigned_user_ids_all = set(pre_assigned_user_ids_all)
    pre_assigned_user_ids_active = set(pre_assigned_user_ids_active)

    protocol = eProtocolProjectInfo.objects.get(pk=prot_id)

    users = get_all_eprotocol_users_active()

    if request.method == 'POST':
        
        some_values = request.POST.getlist('protocol_check_user')

        if len(some_values) > 0:
            
            for i in range(len(some_values)):

                try:
                    temp = eProtocolProjectXUsers.objects.get(eProtocolproject=prot_id, user=int(some_values[i]))
                except eProtocolProjectXUsers.DoesNotExist:
                    temp = None

                if temp:
                    if temp.is_active:
                        pass
                    else:
                        temp.active = True
                        temp.save()
                else:
                    obj = eProtocolProjectXUsers(created_by=request.user, eProtocolproject=eProtocolProjectInfo.objects.get(pk=prot_id), user=User.objects.get(pk=int(some_values[i])))
                    obj.save()

            #this makes the record deactive if user is unchecked
            new_values = set(int(l) for l in some_values)
            for j in pre_assigned_user_ids_all:
                if j in new_values:
                    pass
                else:
                    try:
                        temp = eProtocolProjectXUsers.objects.get(eProtocolproject=prot_id, user=User.objects.get(pk=j))
                        temp.active = False
                        temp.save()
                    except:
                        pass

            #updating project count table
            for k in users:
                try:
                    upc = UserProjectCount.objects.get(user=k.id)
                    upc.project_count = ProjectsXUsers.objects.filter(user=k.id, active=True).count() + eProtocolProjectXUsers.objects.filter(user=k.id, active=True).count()
                    upc.save()
                except UserProjectCount.DoesNotExist:
                    pass

            # recording post assinged users
            post_assigned_user_names_active = eProtocolProjectXUsers.objects.filter(eProtocolproject=prot_id, active=True)
            for i in post_assigned_user_names_active:
                post.append(i.user.username)
                post_assigned_user_emails.append(i.user.email)

            #recording activity log
            event = 'Assign eProtocol'
            record_user_activity_log(
                event       = event, 
                actor       = request.user, 
                proj_name   = protocol.name, 
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

            email_subject = 'Protocol Assignement in CSR.'
            
            for i in range(len(post)):
                if post_assigned_user_emails[i] != '':

                    to_email = post_assigned_user_emails[i]
                    html_content = "<h3>Dear <b>"+ post[i] +"</b>,</h3><br>You have been assinged with a new protocol, <b>" + protocol.name + "</b><br><br><b>Thanks & Regards<br>CSR Automation</b>"

                    email = EmailMessage(subject=email_subject, body=html_content, from_email=from_email, to=[to_email], connection=backend)
                    email.content_subtype = 'html'
                    email_status = email.send()
            
                    # recording Email logs
                    e_log = LogsEmails(

                            event = 'Assign eProtocol',
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
        'protocol' : protocol,
        'pre_assigned_user_ids_active' : pre_assigned_user_ids_active,
    }

    data['html_form'] =  render_to_string('assign_eprotocol.html', context, request=request)
    return JsonResponse(data)


# This view will handle protocol project dashboard
@login_required(login_url='/')
def eProtocolDashboard(request, prot_id):

    protocol = eProtocolProjectInfo.objects.get(pk=prot_id)

    protocol_section = eProtocolProjectSections.objects.filter(eProtocolproject=protocol).order_by('id')

    if request.method == 'POST':

        titlepage_form = EditeProtocolTitlePageForm(request.POST or None, instance=protocol)

        if titlepage_form.is_valid():

            funding_entity_list = ';'.join(request.POST.getlist('funding_entity'))

            obj = titlepage_form.save(commit=False)
            obj.funding_entity = funding_entity_list
            obj.save()

            messages.success(request, 'Data saved!')

        else:
            messages.error(request, 'Something went wrong!')

    else:
        titlepage_form = EditeProtocolTitlePageForm()

    context = {
        'protocol' : protocol,
        'protocol_section' : protocol_section,
        'titlepage_form' : titlepage_form
    }

    return render(request, 'eprotocol_dashboard.html', context)


# This will hanlde the updating section content
@login_required(login_url='/')
def EditeProtocolSection(request, sec_id):

    data = {}

    if request.method == 'POST':

        section = eProtocolProjectSections.objects.get(pk=sec_id)

        section.sec_content = request.POST.get('sec_content')

        section.save()

        data['form_is_valid'] = True

        messages.success(request, "Record updated successfully!")

    else:
        data['form_is_valid'] = False

    return JsonResponse(data)


# This view will handle help/instructions for each section heading
@login_required(login_url='/')
def SectionHelp(request, sec_id):

    data = {}

    proj_sec = eProtocolProjectSections.objects.get(pk=sec_id).sec_heading

    help_sec = eProtocolHelp.objects.get(sec_heading=proj_sec)

    context = {
        'help_sec' : help_sec,
    }

    data['html_form'] = render_to_string('section_help.html', context, request=request)

    return JsonResponse(data)


# This will handle save as template
@login_required(login_url='/')
def SaveasTemplate(request, prot_id):

    protocol = eProtocolProjectInfo.objects.get(pk=prot_id)

    therapeutic_area_list = TherapeuticArea.objects.all()

    data = {}

    if request.method == 'POST':

        code = request.POST.get('temp_code')
        therapeutic_area = request.POST.get('therapeutic_area')

        # Create a new template if not exist if already exists create another template by upgrading version number
        try:
            prot = eProtocolTemplate.objects.filter(code=code, therapeutic_area=therapeutic_area).last()

        except eProtocolTemplate.DoesNotExist:
            prot = None

        if prot:
            new_temp = eProtocolTemplate(code=prot.code, therapeutic_area=prot.therapeutic_area, version_no=str(float(prot.version_no) + 0.001))
            new_temp.created_by = request.user
            new_temp.save()

        else:
            new_temp = eProtocolTemplate(code=code, therapeutic_area=TherapeuticArea.objects.get(pk=therapeutic_area), version_no='0.001')
            new_temp.created_by = request.user
            new_temp.save()

        # Loading the sections content with newly created template
        if new_temp:
            sections_df = pd.DataFrame(list(eProtocolProjectSections.objects.filter(eProtocolproject=protocol).values('sec_heading', 'sec_content', 'read_only')))
            sections_df['template'] = new_temp

            eProtocolTemplateSections.objects.bulk_create(eProtocolTemplateSections(**vals) for vals in sections_df.to_dict('records'))

            new_temp.has_data = True
            new_temp.save()


            messages.success(request, "Protocol saved successfully as Template.")

            return redirect('eprotocol_dashboard', prot_id=prot_id)


    context = {
        'therapeutic_area_list' : therapeutic_area_list,
        'prot_id' : prot_id,
    }

    data['html_form'] = render_to_string('saveas_template.html', context, request=request)

    return JsonResponse(data)


# This view will handle example content for each section heading
@login_required(login_url='/')
def SectionTemplate(request, sec_id):

    data = {}

    proj_sec = eProtocolProjectSections.objects.get(pk=sec_id)

    templates_list = eProtocolTemplate.objects.filter(active=True, delete=False).order_by('-id')

    context = {
        'proj_sec' : proj_sec,
        'templates_list' : templates_list,
    }

    data['html_form'] = render_to_string('section_template.html', context, request=request)

    return JsonResponse(data)

@login_required(login_url='/')
def SectionTemplateContent(request, templt_id, sec_id):

    data = {}

    proj_sec_heading = eProtocolProjectSections.objects.get(pk=sec_id).sec_heading

    try:
        sec_content = eProtocolTemplateSections.objects.get(template=templt_id, sec_heading=proj_sec_heading)
    except eProtocolTemplateSections.DoesNotExist:
        sec_content = None

    context = {
        'sec_content' : sec_content,
    }

    data['html_form'] = render_to_string('section_template_content.html', context, request=request)

    return JsonResponse(data)


@login_required(login_url='/')
def ExportProtocol(request, prot_id):

    doc = GenerateProtocol(request, prot_id)

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    )

    response["Content-Disposition"] = 'attachment; filename = "Reporte.docx"'
    response["Content-Encoding"] = "UTF-8"

    doc.save(response)

    return response

# This view will handle example content for each section heading
@login_required(login_url='/')
def CitationReference(request, pmid, prot_id):

    data = {}

    eProtocolproject = eProtocolProjectInfo.objects.get(pk=prot_id)

    r, created = RefecenceCount.objects.get_or_create(eProtocolproject=eProtocolproject)

    prot_ref_section = eProtocolProjectSections.objects.get(Q(eProtocolproject=eProtocolproject), Q(sec_heading__icontains='References'))

    fetch = PubMedFetcher()

    article = fetch.article_by_pmid(pmid)
    
    r.ref_count += 1
    r.save()

    ref = "<p>" + str(r.ref_count) + ". " + article.citation + "<br>" + "pmid: " + pmid + "</p>"

    if prot_ref_section.sec_content:

        prot_ref_section.sec_content = prot_ref_section.sec_content + ref
    else:
        prot_ref_section.sec_content = ref

    prot_ref_section.save()

    data['ref_count'] = r.ref_count

    context = {
        'prot_id' : prot_id,
    }

    return JsonResponse(data)


@login_required(login_url='/')
def SectionRefrenceSearch(request, prot_id, sec_id):

    data = {}

    context = {
        'prot_id' : prot_id,
        'sec_id' : sec_id
    }

    data['html_form'] = render_to_string('section_refrence_search.html', context, request=request)

    return JsonResponse(data)


@csrf_exempt
@login_required(login_url='/')
def SearchMetapub(request):

    if request.is_ajax():

        data = {}

        # this will return a list with search text and protocol id and section id
        response_data = json.loads(request.body)

        fetch = PubMedFetcher()

        # get the first 5 pmids matching keyword search
        pmids = fetch.pmids_for_query(response_data[0], retmax=1)

        # get articles:
        articles = []
        for pmid in pmids:
            articles.append(fetch.article_by_pmid(pmid))

        context = {
            'articles' : articles,
            'prot_id' : response_data[1],
            'sec_id' : response_data[2]
        }

        data['html_form'] = render_to_string('section_reference.html', context, request=request)

        return JsonResponse(data)

