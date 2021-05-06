import os
import pandas as pd
import numpy as np
from datetime import datetime
import logging
import traceback
import re

from docx import Document


from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import *
from .admin_csr_mapping import get_all_headings

User = get_user_model()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

csr_logger = logging.getLogger('csr')
csr_except_logger = logging.getLogger('csr_except')


def get_all_users():
	users = User.objects.all()
	return users


def get_all_users_active():
	users = User.objects.filter(is_active=True)
	return users

def get_all_csr_users_active():
	users = User.objects.filter(Q(user_role__role='CSR User') | Q(user_role__role='Global User'), is_active=True)
	return users


def get_all_eprotocol_users_active():
	users = User.objects.filter(Q(user_role__role='eProtocol User') | Q(user_role__role='Global User'), is_active=True)
	return users


def get_all_project_list():
	projects = ProjectInfo.objects.all()
	return projects
	

def check_file_content(document):
	
	try:

		# calling procedure from admin_csr_mapping
		headings = get_all_headings(document)
		wrg__frmt = ''
		for i in headings:
			if re.match("^\d+(?:\.\d*)*(?![\w-])", i):
				wrg__frmt += i
				break

		return wrg__frmt

	except Exception as e:
		csr_except_logger.critical(str(e) + '\n' + str(traceback.format_exc()))


#to record activity log
def record_user_activity_log(event, actor, **kwargs):

	raw_message = ActivityLogEvents.objects.get(event=event).message

	if event == 'Add User':
		temp_message = str(actor) + ' ' + raw_message.replace('#', kwargs.get('dif_user'))
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'Activate User':
		temp_message = str(actor) + ' ' + raw_message.replace('#', kwargs.get('dif_user'))
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'Deactivate User':
		temp_message = str(actor) + ' ' + raw_message.replace('#', kwargs.get('dif_user'))
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'Create Project':
		temp_message = str(actor) + ' ' + raw_message.replace('#', kwargs.get('proj_name'))
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'Assign Project':
		temp_message = str(actor) + ' ' + raw_message.replace('#', kwargs.get('proj_name'))
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'Assign eProtocol':
		temp_message = str(actor) + ' ' + raw_message.replace('#', kwargs.get('proj_name'))
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'CSR Upload':
		temp_message = str(actor) + ' ' + raw_message
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'Edit Project':
		temp_message = raw_message.replace('#', kwargs.get('proj_name')) + ' by ' + str(actor)
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'Protocol Upload':
		temp_message = str(actor) + ' ' + raw_message.replace('#', kwargs.get('proj_name'))
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'SAR Upload':
		temp_message = str(actor) + ' ' + raw_message.replace('#', kwargs.get('proj_name'))
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'Upload Protocol':
		temp_message = str(actor) + ' ' + raw_message
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'Upload SAR':
		temp_message = str(actor) + ' ' + raw_message
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'Custom CSR Upload':
		temp_message = str(actor) + ' ' + raw_message.replace('#', kwargs.get('proj_name'))
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'Generate CSR':
		temp_message = str(actor) + ' ' + raw_message.replace('#', kwargs.get('proj_name'))
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'Edit Custom CSR':
		temp_message = str(actor) + ' ' + raw_message.replace('#', kwargs.get('proj_name'))
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'CSR Mapping':
		temp_message = str(actor) + ' ' + raw_message
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()

	elif event == 'Resend Email':
		temp_message = str(actor) + ' ' + raw_message.replace('#', kwargs.get('email')).replace('$', kwargs.get('log_event'))
		log_model 	 = LogsActivity(
			event 	 = event,
			message  = temp_message,
			userid 	 = actor.id,
			sessionid= kwargs.get('session_id')
			)
		log_model.save()



def filtered_pre_mapped_admin_data():

	pre_mapped_headings = list(GlobalMappingTable.objects.all().values())

	dataframe = pd.DataFrame(pre_mapped_headings, columns=['csr_heading', 'source_file', 'copy_headings', 'parent_id'])
	
	dataframe = dataframe.replace(r'^\s*$', np.nan, regex=True)
	dataframe = dataframe.dropna()
	
	Dframe = dataframe.to_dict(orient='records')

	return Dframe



def csr_updated_admin_form_data(csr_headings_data, source_data, copy_headings_data, parent_ids, pre_mapped_headings):

	try:

		data = {
			'csr_heading' : csr_headings_data,
			'source_file' : source_data,
			'copy_headings' : copy_headings_data,
			'parent_id' : parent_ids
		}

		dataframe = pd.DataFrame(data, columns=['csr_heading', 'source_file', 'copy_headings', 'parent_id'])
		dataframe = dataframe.drop(dataframe[(dataframe['parent_id'] != '0') & ((dataframe['source_file'] == '') | (dataframe['copy_headings'] == ''))].index)
		dataframe = dataframe.replace(r'^\s*$', np.nan, regex=True)
		dataframe = dataframe.dropna()

		CDframe = pd.DataFrame(pre_mapped_headings)

		Only_updated = pd.concat([dataframe, CDframe]).drop_duplicates(keep=False)

		Dframe = Only_updated.to_dict(orient='records')

		return Dframe
		
	except Exception as e:
		csr_except_logger.critical(str(e) + '\n' + str(traceback.format_exc()))



def global_mapping_table_structure(mapping_table):
	dicT = {}

	for i in mapping_table:
		if i.parent_id == '0':
			ch_cont = GlobalMappingTable.objects.filter(csr_heading = i.csr_heading, parent_id=i.csr_heading).count()
			dicT[i.csr_heading] = ch_cont

	return dicT