from django.urls import path
from . import views

urlpatterns = [
	path('manage_protocol_template/', views.ManageProtocolTemplate, name='manage_protocol_template'),
	path('create_protocol_template/', views.CreateProtocolTemplate, name='create_protocol_template'),
	path('create_eprotocol/<usr_id>', views.CreateProtocol, name='create_eprotocol'),
	path('edit_eprotocol/<prot_id>', views.EditeProtocol, name='edit_eprotocol'),

	path('add_etemplate_content/<templt_id>', views.AddContentToTemplate, name='add_etemplate_content'),
	path('delete_etemplate/<templt_id>', views.DeleteTemplate, name='delete_etemplate'),
	path('view_etemplate_sections/<templt_id>', views.ViewTemplateSection, name='view_etemplate_sections'),
	path('etemplate_sections/<sec_id>', views.EditTemplateSection, name='etemplate_sections'),

	path('archive_eprotocol/<prot_id>', views.ArchiveProtocol, name='archive_eprotocol'),
	path('unarchive_eprotocol/<prot_id>', views.UnarchiveProtocol, name='unarchive_eprotocol'),
	path('clone_eprotocol/<prot_id>', views.CloneProtocol, name='clone_eprotocol'),
	path('assign_eprotocol/<prot_id>', views.AssigneProtocolProject, name='assign_eprotocol'),

	path('eprotocol_dashboard/<prot_id>', views.eProtocolDashboard, name='eprotocol_dashboard'),

	path('eprotocol_sections/<sec_id>', views.EditeProtocolSection, name='eprotocol_sections'),

	path('section_help/<sec_id>', views.SectionHelp, name='section_help'),

	path('section_ref_search/<prot_id>/<sec_id>', views.SectionRefrenceSearch, name='section_ref_search'),

	path('search_metapub/>', views.SearchMetapub, name='search_metapub'),

	path('citation_reference/<pmid>/<prot_id>', views.CitationReference, name='citation_reference'),

	path('save_as_temp/<prot_id>', views.SaveasTemplate, name='save_as_temp'),

	path('section_template/<sec_id>', views.SectionTemplate, name='section_template'),
	path('section_template_content/<templt_id>/<sec_id>', views.SectionTemplateContent, name='section_template_content'),


	path('export_protocol/<prot_id>', views.ExportProtocol, name='export_protocol'),

]