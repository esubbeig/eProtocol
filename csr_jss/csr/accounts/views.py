import logging
import os
import traceback

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail.backends.smtp import EmailBackend
from django.core.mail import EmailMessage, get_connection, EmailMultiAlternatives
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth import get_user_model
from django.conf import settings

from .forms import *
from .models import *
from .token_generator import *
from .data_encrypt import *

from core.models import UserProjectCount, LogsEmails, EmailConfiguration
from core.admin_operations import *
from audits.audit import *

User = get_user_model()

csr_logger = logging.getLogger('info.log')
csr_except_logger = logging.getLogger('error.log')


@login_required(login_url='/')
def CreateuserView(request):

    data = {}

    #to send confirmation mail
    try:
        config  = EmailConfiguration.objects.last()
    except EmailConfiguration.DoesNotExist:
        config = None

    if request.method == 'POST':

        role = request.POST.get('user_role')

        form = CreateUserForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False

            # if role == 'Global User':
                # user.user_role = Roles.objects.get(pk=1)
            # elif role == 'CSR User':
                # user.user_role = 2
                # user.user_role = Roles.objects.get(pk=2)
            # elif role == 'eProtcol User':
                # user.user_role = 3
                # user.user_role = Roles.objects.get(pk=3)

            user.user_role = Roles.objects.get(role=role)

            user.created_by = request.user
            user.set_unusable_password()
            user.save()

            # Updating the ProjectXCount modal
            temp_count = UserProjectCount(user=user)
            temp_count.save()

            
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
            email_subject = 'Activate Your Account with CSR'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = account_activation_token.make_token(user)
            activation_link = "{0}/accounts/set_password/?uid={1}".format(current_site, uid)
            # message = "Dear {0},\n {1}" .format(user.username, activation_link)
            to_email = form.cleaned_data.get('email')
            html_content = "<h3>Dear <b>"+ user.username +"</b>,</h3><br>A new account was created with CSR. To make use of your account, first you need to set the password. Please follow the below link.<br><br>"+ activation_link + "<br><br><b>Thanks & Regards<br>CSR Automation</b>"
            # html_content = "hello"
            email = EmailMessage(subject=email_subject, body=html_content, from_email=from_email, to=[to_email], connection=backend)
            email.content_subtype = 'html'
            email_status = email.send()

            # recording Email logs
            e_log = LogsEmails(

                    event = 'Create User',
                    to_email = to_email,
                    from_email = from_email,
                    subject = email_subject,
                    message_body = html_content,
                    email_sent = email_status,
                    created_by = request.user

                )
            if email_status:
                e_log.email_response = "Email sent scuccessfully"
                data['mail_status'] = True
                messages.success(request, "Confirmation mail send to the registered mail! Please activate")
                
            else:
                e_log.email_response = "Not able to connect SMTP server"
                data['mail_status'] = False
                messages.error(request, "Problem with connecting SMTP server. Please check the Email Configurations!")
                # recording logging
                csr_except_logger.critical("Not able to connect SMTP server while creating " + user.username)

            e_log.save()

            #recording activity log
            event = 'Add User'
            record_user_activity_log(
                event       = event,
                actor       = request.user, 
                dif_user    = user.username, 
                session_id  = request.session.session_key
                )

            data['form_is_valid'] = True

        else:
            data['form_is_valid'] = False

    else:
        form = CreateUserForm()

    context = {
        'form' : form,
        'config' : config,
    }
    data['html_form'] = render_to_string('registration/create_user.html', context, request=request)
    return JsonResponse(data)


# to set the password first time when user is created
def SetPasswordView(request):

    uidb64 = request.GET.get('uid')
    uid = force_bytes(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    if user is not None:

        if user.has_usable_password():

            return HttpResponse('Sorry, You have already set your password. Please contact Admin!')
        
        else:

            status = 0
            user.is_active = True
            user.save()
            login(request, user)
    
            if request.method == 'POST':

                password = request.POST.get('new_password1')

                form = SetPasswordForm(request.user, request.POST)

                if form.is_valid():
                    user = form.save()
                    update_session_auth_hash(request, user)
                    
                    # storing encrypted password in another table
                    encrypted_password = encrypt_message(password)
                    obj, created =  CredInfo.objects.get_or_create(user=request.user)
                    obj.key_pass = encrypted_password
                    obj.save()

                    logout(request)

                    return render(request, 'registration/set_password_success.html')
                    status = 1

                else:
                    pass

            else:
                form = SetPasswordForm(request.user)

            if status == 0:
                user.is_active = False
                user.save()

            return render(request, 'registration/activate_set_password.html', {'form' : form})


# to reset the password if user forgets the password
def ResetPasswordView(request):
    uidb64 = request.GET.get('uid')
    uid = force_bytes(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=uid)

    if user is not None:

        if user.is_active:

            login(request, user)
            
            if request.method == 'POST':

                password = request.POST.get('new_password1')

                form = SetPasswordForm(request.user, request.POST)

                if form.is_valid():

                    user = form.save()
                    update_session_auth_hash(request, user)

                    # storing encrypted password in another table
                    encrypted_password = encrypt_message(password)
                    obj, created =  CredInfo.objects.get_or_create(user=request.user)
                    obj.key_pass = encrypted_password
                    obj.save()

                    logout(request)
                    return render(request, 'registration/reset_password_success.html')

                else:
                    # messages.error(request, 'Passwords mismatched!')
                    pass

            else:
                form = SetPasswordForm(request.user)

            return render(request, 'registration/reset_password.html', {'form' : form})

        else:
            return HttpResponse('Sorry, Your account has been disabled, please contact Admin!')


def ForgotPasswordView(request):

    if request.method == 'POST':

        to_email = request.POST['email']

        try:
            user = User.objects.get(email=to_email)
        except User.DoesNotExist:
            user = None


        if user is not None:

            if user.is_active:

                #to send forgot password mail
                config  = EmailConfiguration.objects.last()
                backend = EmailBackend(

                    host          = config.email_host,
                    username      = config.email_host_user,
                    password      = config.email_host_password,
                    port          = config.email_port,
                    use_tls       = True,
                    fail_silently = True
                )
                from_email            = config.email_default_mail
                current_site          = get_current_site(request)
                email_subject         = 'Reset your Account Password with CSR'
                uid                   = urlsafe_base64_encode(force_bytes(user.pk))
                password_reset_link   = "{0}/reset_password/?uid={1}".format(current_site, uid)
                html_content          = "<h3>Dear <b>"+ user.username +"</b>,</h3><br>We got a request to reset your password with CSR. Please follow the below link.<br><br>"+ password_reset_link + "<br><br><b>Thanks & Regards<br>CSR Automation</b>"
                email                 = EmailMessage(subject=email_subject, body=html_content, from_email=from_email, to=[to_email], connection=backend)
                email.content_subtype = 'html'
                email_status          = email.send()

                # recording Email logs
                e_log = LogsEmails(

                        event        = 'Forgot Password',
                        to_email     = to_email,
                        from_email   = from_email,
                        subject      = email_subject,
                        message_body = html_content,
                        email_sent   = email_status,
                        created_by   = User.objects.get(email=to_email)
                    )
                if email_status:
                    e_log.email_response = "Email sent scuccessfully"

                else:
                    e_log.email_response = "Not able to connect SMTP server"                    

                e_log.save()

                if email_status:
                    messages.success(request, 'A password reset link has been sent to your email')
                else:
                    messages.error(request, 'Failed! to send reset password link. Please try after some time.')

            else:
                messages.error(request, 'Sorry, Your account has been disabled. Please contact Admin!')

        else:
            messages.error(request, 'No user found with given email')
            

    return render(request, 'registration/forgot_password.html')

def LoginView(request):
    if request.user.is_authenticated:
        pass
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        messages.success(request, "You are logged in as " + username)
                        return redirect('home')
                        
                    else:
                        messages.error(request, "Your account is disabled!")
                else:
                    messages.error(request, 'Invalid username or password')
            else:
                messages.error(request, 'Invalid username or password')
        else:
            form = AuthenticationForm()

        return render(request, 'registration/login.html', {'form' : form})


@login_required(login_url='/')
def LogoutView(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/')
def ChangePasswordView(request):

    data = {}

    if request.method == 'POST':

        form = PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():

            updated_pass = request.POST.get('new_password1')

            user = form.save()
            update_session_auth_hash(request, user)

            # storing passwords seperately in another table
            encrypted_password = encrypt_message(updated_pass)
            obj, created =  CredInfo.objects.get_or_create(user=request.user)
            obj.key_pass = encrypted_password
            obj.save()

            messages.success(request, "Password changed successfully")

            data['form_is_valid'] = True

        else:
            data['form_is_valid'] = False
    else:
        form = PasswordChangeForm(request.user)
        
    context = {
        'form' : form
    }
    data['html_form'] = render_to_string('registration/change_password.html', context, request=request)
    return JsonResponse(data)


#to activate the users
@login_required(login_url='/')
def ActivateUserView(request, usr_id):

    if request.is_ajax():

        data = {}

        usr = User.objects.get(pk=usr_id)

        if usr.has_usable_password():

            usr.is_active = True
            usr.save()

            #recording user acivity log
            event = 'Activate User'
            record_user_activity_log(
                event       = event, 
                actor       = request.user, 
                dif_user    = usr.username, 
                session_id  = request.session.session_key
                )
            data['status'] = True

        else:
            data['status'] = False
        
        return JsonResponse(data)


#to deactivate the users
@login_required(login_url='/')
def DeactivateUserView(request, usr_id):

    if request.is_ajax():

        data = {}

        usr = User.objects.get(pk=usr_id)
        usr.is_active = False
        usr.save()

        #recording user acivity log
        event = 'Deactivate User'
        record_user_activity_log(
            event       = event, 
            actor       = request.user, 
            dif_user    = usr.username, 
            session_id  = request.session.session_key
            )
        
        data['status'] = True

        return JsonResponse(data)