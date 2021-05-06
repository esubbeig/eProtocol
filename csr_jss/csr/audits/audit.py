import numpy as np
import pandas as pd

from django.forms.models import model_to_dict

from .models import *


# audit log for user's edit eProtocol
def Edit_eProtocol_Log(previoust_state, current_state, project, user, client_ip):

	action = 'Edit eProtocol'

	rm_keys = ['id', 'upin', 'nct', 'study_type', 'funding_entity', 'ind_sponsor', 'archived', 'active', 'delete', 'created_by']

	# conveting to dictionary from model instalce
	pre_dict_obj = model_to_dict(previoust_state)
	cur_dict_obj = model_to_dict(current_state)

	# replacing id with the name
	pre_dict_obj['therapeutic_area'] = previoust_state.therapeutic_area.therapeutic_area
	cur_dict_obj['therapeutic_area'] = current_state.therapeutic_area.therapeutic_area

	# popping keys which are not required
	[pre_dict_obj.pop(key) for key in rm_keys]
	[cur_dict_obj.pop(key) for key in rm_keys]

	audit_model = AuditLog(

			user 		   = user,
			module 		   = 'eProtocol',
			project 	   = project.name,
			action	  	   = action,
			previous_state = pre_dict_obj,
			current_state  = cur_dict_obj,
			ip 			   = client_ip
		)
	audit_model.save()


# audit log for user's edit project
def edit_project_log(previoust_state, current_state, project, user, client_ip):

	action = 'Edit Project'

	rm_keys = ['id', 'active', 'delete', 'created_by', 'generated']

	# conveting to dictionary from model instalce
	pre_dict_obj = model_to_dict(previoust_state)
	cur_dict_obj = model_to_dict(current_state)

	# replacing id with the name
	pre_dict_obj['therapeutic_area'] = previoust_state.therapeutic_area.therapeutic_area
	cur_dict_obj['therapeutic_area'] = current_state.therapeutic_area.therapeutic_area

	# popping keys which are not required
	[pre_dict_obj.pop(key) for key in rm_keys]
	[cur_dict_obj.pop(key) for key in rm_keys]

	audit_model = AuditLog(

			user 		   = user,
			module 		   = 'CSR',
			project 	   = project.project_name,
			action	  	   = action,
			previous_state = pre_dict_obj,
			current_state  = cur_dict_obj,
			ip 			   = client_ip
		)
	audit_model.save()


# audit log for admin assing projects
def assign_project_log(pre_assinged, post_assinged, user, client_ip):

	action = 'Assign Project'

	audit_model = AuditLog(

			user 		   = user,
			module 		   = 'CSR',
			action		   = action,
			previous_state = pre_assinged,
			current_state  = post_assinged,
			ip 			   = client_ip,
		)
	audit_model.save()


# audit log for user's custom csr mapping
def edit_custom_csr_mapping_log(custom_mapping, csr_headings_data, source_data, copy_headings_data, reason, user, project, client_ip):

	action = 'Edit Mapping'
	
	new_custom_mapping = [{k: v for k, v in d.items() if k != 'id' and k != 'project_id' and k != 'created_by_id'} for d in custom_mapping]
		
	pre_mapped_dataframe = pd.DataFrame(new_custom_mapping, columns=['csr_heading', 'source_file', 'copy_headings'])

	# print(pre_mapped_dataframe)

	pre_mapped_dataframe = pre_mapped_dataframe.replace(r'^\s*$', np.nan, regex=True)
	pre_mapped_dataframe = pre_mapped_dataframe.dropna()

	pre_mapped_dataframe_dict = pre_mapped_dataframe.to_dict(orient='records')
	
	data = {
		'csr_heading' : csr_headings_data,
		'source_file' : source_data,
		'copy_headings' : copy_headings_data
	}

	dataframe = pd.DataFrame(data, columns=['csr_heading', 'source_file', 'copy_headings'])
	dataframe = dataframe.replace(r'^\s*$', np.nan, regex=True)
	dataframe = dataframe.dropna()

	dataframe_dict = dataframe.to_dict(orient='records')

	audit_model = AuditLog(

			user 		   = user,
			module 		   = 'CSR',
			project 	   = project.project_name,
			action		   = action,
			previous_state = pre_mapped_dataframe_dict,
			current_state  = dataframe_dict,
			ip 			   = client_ip,
			reason 		   = reason
		)
	audit_model.save()


# audit log for admin's global csr mapping
def edit_global_csr_mapping_log(pre_mapped_headings, csr_headings_data, source_data, copy_headings_data, reason, user, client_ip):

	action = 'Edit Mapping'
	
	new_pre_mapped_headings = [{k: v for k, v in d.items() if k != 'id'} for d in pre_mapped_headings]

	pre_mapped_dataframe = pd.DataFrame(new_pre_mapped_headings, columns=['csr_heading', 'source_file', 'copy_headings'])

	# print(pre_mapped_dataframe)

	pre_mapped_dataframe = pre_mapped_dataframe.replace(r'^\s*$', np.nan, regex=True)
	pre_mapped_dataframe = pre_mapped_dataframe.dropna()

	pre_mapped_dataframe_dict = pre_mapped_dataframe.to_dict(orient='records')

	data = {
		'csr_heading' : csr_headings_data,
		'source_file' : source_data,
		'copy_headings' : copy_headings_data
	}

	dataframe = pd.DataFrame(data, columns=['csr_heading', 'source_file', 'copy_headings'])
	dataframe = dataframe.replace(r'^\s*$', np.nan, regex=True)
	dataframe = dataframe.dropna()

	dataframe_dict = dataframe.to_dict(orient='records')

	audit_model = AuditLog(

			user 		   = user,
			module 		   = 'CSR',
			action		   = action,
			previous_state = pre_mapped_dataframe_dict,
			current_state  = dataframe_dict,
			ip 			   = client_ip,
			reason 	       = reason
		)
	audit_model.save()