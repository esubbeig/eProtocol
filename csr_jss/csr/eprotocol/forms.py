from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import *


class CreateProtocolTemplateForm(forms.ModelForm):

	class Meta:
		model = eProtocolTemplate
		fields = ('code', 'therapeutic_area',)

	# def clean_name(self):
	# 	name = self.cleaned_data['name']
	# 	if name and eProtocolTemplate.objects.filter(name__iexact=name.strip().lower()).count() > 0:
	# 		raise forms.ValidationError(u'This name is already registered.')
	# 	return name

	def clean_code(self):
		code = self.cleaned_data['code']
		if code and eProtocolTemplate.objects.filter(code__iexact=code.strip().lower()).count() > 0:
			raise forms.ValidationError(u'This code is already registered.')
		return code


class SaveAsTemplateForm(forms.ModelForm):

	class Meta:
		model = eProtocolTemplate
		fields = ('code', 'therapeutic_area',)


class CreateProtocolForm(forms.ModelForm):

	class Meta:
		model = eProtocolProjectInfo
		fields = ('code', 'name', 'short_name', 'therapeutic_area', 'sub_speciality', 'template',)

	def clean_code(self):
		code = self.cleaned_data['code']

		if code and eProtocolProjectInfo.objects.filter(code__iexact=code.strip().lower()).count() > 0:
			raise forms.ValidationError(u'This code is already existed.')
		return code

	def clean_name(self):
		name = self.cleaned_data['name']

		if name and eProtocolProjectInfo.objects.filter(name__iexact=name.strip().lower()).count() > 0:
			raise forms.ValidationError(u'This name is already existed.')
		return name


class EditeProtocolForm(forms.ModelForm):

	class Meta:
		model = eProtocolProjectInfo
		fields = ('code', 'name', 'short_name', 'therapeutic_area', 'sub_speciality',)

	def clean_code(self):
		code = self.cleaned_data['code']

		if code and eProtocolProjectInfo.objects.filter(code__iexact=code.strip().lower()).count() > 1:
			raise forms.ValidationError(u'This code is already existed.')
		return code

	def clean_name(self):
		name = self.cleaned_data['name']

		if name and eProtocolProjectInfo.objects.filter(name__iexact=name.strip().lower()).count() > 1:
			raise forms.ValidationError(u'This name is already existed.')
		return name


class CloneProtocolForm(forms.ModelForm):

	class Meta:
		model = eProtocolProjectInfo
		fields = ('code', 'name', 'short_name',)

	def clean_code(self):
		code = self.cleaned_data['code']

		if code and eProtocolProjectInfo.objects.filter(code__iexact=code.strip().lower()).count() > 0:
			raise forms.ValidationError(u'This code is already existed.')
		return code

	def clean_name(self):
		name = self.cleaned_data['name']

		if name and eProtocolProjectInfo.objects.filter(name__iexact=name.strip().lower()).count() > 0:
			raise forms.ValidationError(u'This name is already existed.')
		return name


class TemplateContentFileForm(forms.Form):
	file = forms.FileField()

	def clean_file(self):
		filename = self.cleaned_data['file'].name
		if filename:
			if filename.endswith('.csv') or filename.endswith('.xlsx'):
				pass
			else:
				raise forms.ValidationError(u'Trying to upload wrong extensions.')
		return filename


class EditeProtocolTitlePageForm(forms.ModelForm):

	class Meta:
		model = eProtocolProjectInfo
		fields = ('code', 'name', 'short_name', 'upin', 'nct', 'study_type', 'funding_entity', 'ind_sponsor')

	def clean_code(self):
		code = self.cleaned_data['code']

		if code and eProtocolProjectInfo.objects.filter(name__iexact=code.strip().lower()).count() > 1:
			raise forms.ValidationError(u'This code is already existed.')
		return code

	def clean_name(self):
		name = self.cleaned_data['name']

		if name and eProtocolProjectInfo.objects.filter(name__iexact=name.strip().lower()).count() > 1:
			raise forms.ValidationError(u'This name is already existed.')
		return name


class MakeasTemplateForm(forms.ModelForm):

	class Meta:
		model = eProtocolTemplate
		fields = ('code', 'therapeutic_area',)

	def clean_code(self):
		code = self.cleaned_data['code']
		if code and eProtocolTemplate.objects.filter(name__iexact=code.strip().lower()).count() > 0:
			raise forms.ValidationError(u'This code is already registered.')
		return code