import pandas as pd

from .models import *

def ImportContentToModel(request, file, templt_id):

	try:
		template = eProtocolTemplate.objects.get(pk=templt_id)
	except:
		template = None

	status = 0

	if file.name.endswith('.csv'):

		dataframe = pd.read_csv(file)

	elif file.name.endswith('.xlsx'):

		dataframe = pd.read_excel(file, engine="openpyxl")

	elif file.name.endswith('.xls'):

		dataframe = pd.read_excel(file, engine="xlrd")

	if not dataframe.empty:

		# dataframe = dataframe.iloc[:3]

		dataframe['read_only'] = dataframe['read_only'].fillna(0)

		dataframe = dataframe.astype({'read_only' : 'int'})

		dataframe['template'] = template

		eProtocolTemplateSections.objects.bulk_create(eProtocolTemplateSections(**vals) for vals in dataframe.to_dict('records'))

		template.has_data = True
		template.save()

	status = 1

	return status

def CopyTemplateContentToeProtocolModel(dataframe, epro_obj):

	status = 0

	if not dataframe.empty:

		dataframe['eProtocolproject'] = epro_obj

		eProtocolProjectSections.objects.bulk_create(eProtocolProjectSections(**vals) for vals in dataframe.to_dict('records'))

	status = 1

	return status


def CloneProtocolContent(dataframe, epro_obj):

	status = 0

	if not dataframe.empty:

		dataframe['eProtocolproject'] = epro_obj

		eProtocolProjectSections.objects.bulk_create(eProtocolProjectSections(**vals) for vals in dataframe.to_dict('records'))

	status = 1

	return status

