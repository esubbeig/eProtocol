from datetime import datetime
import pandas as pd
import numpy as np

from django.contrib.auth.models import User

from .models import *
from eprotocol.models import *

def get_user_projects(usr):
	projects = ProjectsXUsers.objects.filter(user=usr, active=True)
	return projects


def get_user_eprotocol(usr):
	projects = eProtocolProjectXUsers.objects.filter(user=usr, active=True)
	return projects

def csr_updated_user_form_data(csr_headings_data, source_data, copy_headings_data, parent_ids):

	data = {
		'csr_heading' : csr_headings_data,
		'source_file' : source_data,
		'copy_headings' : copy_headings_data,
		'parent_id' : parent_ids,
	}

	dataframe = pd.DataFrame(data, columns=['csr_heading', 'source_file', 'copy_headings', 'parent_id'])
	dataframe = dataframe.drop(dataframe[(dataframe['parent_id'] != '0') & ((dataframe['source_file'] == '') | (dataframe['copy_headings'] == ''))].index)
	dataframe = dataframe.replace(r'^\s*$', np.nan, regex=True)
	dataframe = dataframe.dropna()

	Dframe = dataframe.to_dict(orient='records')
	# print(Dframe)
	return Dframe
	
	# print(dataframe)



def get_global_mapping_suggestions(csr_headings, protocol_headings, sar_headings):

	global_pre_mapped_headings = list(GlobalMappingTable.objects.all().values())

	filtered_global_pre_mapped_headings = []

	filtered_global_pre_mapped_headings_parent = []


	if len(protocol_headings) != 0 and len(sar_headings) != 0:
		
		for i in csr_headings:
			for j in range(len(global_pre_mapped_headings)):
				if (i == global_pre_mapped_headings[j]['csr_heading'] and global_pre_mapped_headings[j]['source_file'] != '' and global_pre_mapped_headings[j]['copy_headings'] != ''):
					filtered_global_pre_mapped_headings.append(global_pre_mapped_headings[j])

					if (i == global_pre_mapped_headings[j]['csr_heading'] and global_pre_mapped_headings[j]['source_file'] != '' and global_pre_mapped_headings[j]['copy_headings'] != '' and global_pre_mapped_headings[j]['parent_id'] == '0'):
						filtered_global_pre_mapped_headings_parent.append(global_pre_mapped_headings[j])
	else:
		
		if len(protocol_headings) != 0:
			
			for i in csr_headings:
				for j in range(len(global_pre_mapped_headings)):
					if (i == global_pre_mapped_headings[j]['csr_heading'] and global_pre_mapped_headings[j]['source_file'] == 'Protocol' and global_pre_mapped_headings[j]['copy_headings'] != ''):
						filtered_global_pre_mapped_headings.append(global_pre_mapped_headings[j])

						if (i == global_pre_mapped_headings[j]['csr_heading'] and global_pre_mapped_headings[j]['source_file'] == 'Protocol' and global_pre_mapped_headings[j]['copy_headings'] != '' and global_pre_mapped_headings[j]['parent_id'] == '0'):
							filtered_global_pre_mapped_headings_parent.append(global_pre_mapped_headings[j])

		elif len(sar_headings) != 0:
			
			for i in csr_headings:
				for j in range(len(global_pre_mapped_headings)):
					if (i == global_pre_mapped_headings[j]['csr_heading'] and global_pre_mapped_headings[j]['source_file'] == 'SAR' and global_pre_mapped_headings[j]['copy_headings'] != ''):
						filtered_global_pre_mapped_headings.append(global_pre_mapped_headings[j])

						if (i == global_pre_mapped_headings[j]['csr_heading'] and global_pre_mapped_headings[j]['source_file'] == 'SAR' and global_pre_mapped_headings[j]['copy_headings'] != '' and global_pre_mapped_headings[j]['parent_id'] == '0'):
							filtered_global_pre_mapped_headings_parent.append(global_pre_mapped_headings[j])

	return filtered_global_pre_mapped_headings, filtered_global_pre_mapped_headings_parent

