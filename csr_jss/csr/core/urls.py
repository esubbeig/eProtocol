from django.urls import path, include
from django.contrib import admin
from . import views


urlpatterns = [
    path('', views.home, name='home'),
	path('global_csr_upload/', views.global_csr_upload, name='global_csr_upload'),
    path('upload_csr_admin/', views.upload_csr_admin, name='upload_csr_admin'),
    path('upload_protocol_admin/', views.upload_protocol_admin, name='upload_protocol_admin'),
    path('upload_sar_admin/', views.upload_sar_admin, name='upload_sar_admin'),
    path('csr_mapping/', views.csr_mapping, name='csr_mapping'),

    path('csr_mapping/ad_on_change_protocol_headings', views.ad_on_change_protocol_headings, name='ad_on_change_protocol_headings'),
    path('csr_mapping/ad_on_change_sar_headings', views.ad_on_change_sar_headings, name='ad_on_change_sar_headings'),
    path('csr_mapping/ad_csr_headings', views.ad_csr_headings, name='ad_csr_headings'),

    path('usr_on_change_protocol_headings/<p_id>', views.usr_on_change_protocol_headings, name='usr_on_change_protocol_headings'),
    path('usr_on_change_sar_headings/<p_id>', views.usr_on_change_sar_headings, name='usr_on_change_sar_headings'),
    path('usr_csr_headings/<p_id>', views.usr_csr_headings, name='usr_csr_headings'),

	path('create_project/<usr_id>', views.create_project, name='create_project'),
    path('get_projects_admin/', views.get_projects_admin, name='get_projects_admin'),
    
    path('get_all_users_details/', views.get_all_users_details, name='get_all_users_details'),
    path('get_all_active_users_details/', views.get_all_active_users_details, name='get_all_active_users_details'),
    path('get_all_act_inact_users_details/', views.get_all_act_inact_users_details, name='get_all_act_inact_users_details'),
    
    path('edit_user_project/<usr_id>/<proj_id>', views.edit_user_project, name='edit_user_project'),
    path('project_dashboard/<usr_id>/<proj_id>', views.project_dashboard, name='project_dashboard'),
    path('csr_upload/<usr_id>/<pro_id>', views.csr_upload, name='csr_upload'),
    path('protocol_file_upload/<usr_id>/<pro_id>', views.protocol_file_upload, name='protocol_file_upload'),
    path('sar_file_upload/<usr_id>/<pro_id>', views.sar_file_upload, name='sar_file_upload'),
    path('download/<path>', views.download, name='download'),
    path('assign_project/<prj_id>', views.assign_project_new, name='assign_project'),
    
    path('activity_log/<usr_id>', views.activity_log, name='activity_log'),
    path('activity_log_on_change/<usr_id>', views.activity_log_on_change, name='activity_log_on_change'),
    path('display_global_csr_mapping/', views.display_global_csr_mapping, name='display_global_csr_mapping'),
    path('generate_csr/<usr_id>/<proj_id>', views.generate_csr, name='generate_csr'),
    path('edit_csr_mapping/<usr_id>/<proj_id>/', views.edit_csr_mapping, name='edit_csr_mapping'),

    path('search_user_project/', views.search_user_project, name='search_user_project'),
    path('search_admin_project/', views.search_admin_project, name='search_admin_project'),
    
    path('audit_log/<usr_id>', views.audit_log, name='audit_log'),
    path('audit_log_on_change/<usr_id>', views.audit_log_on_change, name='audit_log_on_change'),

    path('confirm_csr_mapping_user/<usr_id>/<proj_id>', views.confirm_csr_mapping_user, name='confirm_csr_mapping_user'),
    path('confirm_csr_mapping_admin/', views.confirm_csr_mapping_admin, name='confirm_csr_mapping_admin'),

    path('email_configuration/', views.email_configuration, name='email_configuration'),
    path('mail_logs/', views.mail_logs, name='mail_logs'),
    path('resend_email/<mail_id>', views.resend_email, name='resend_email'),

    path('display_logging/', views.display_logging, name='display_logging'),

    path('release_note/', views.release_note, name='release_note'),
]


