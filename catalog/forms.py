from dataclasses import dataclass, fields
from pyexpat import model
from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from catalog.models import BookInstance
class RenewBook(forms.Form):
	renewal_date = forms.DateField(help_text='Enter a date between now and 4 weeks.')

	def clean_renewal_date(self):
		data = self.cleaned_data['renewal_date']

		# check date not in the past
		if data < datetime.date.today():
			raise ValidationError(_('Invalid date - Renewal in past'))

		# check if date if it is in the correct range (4 weeks ahead)
		if data > datetime.date.today() + datetime.timedelta(weeks=4):
			raise ValidationError(_('Invalid Date - Renewal more than 4 weeks ahead'))
		
		return data
		

# MODELFORM *********************************************

# class RenewBook(ModelForm):
# 	class Meta:
# 		model = BookInstance
# 		fields = ['due_back', ]
# 		labels = {'due_back': _('New renewal date')}
# 		help_text = {'due_date': _('Enter a date between now and 4 weeks.')}
# 
# 		def clean_due_back(self):
# 			data = self.cleaned_data['due_back']
# 
# 			# check if not in the past
# 			if data < datetime.date.today():
# 				raise ValidationError(_('Cannot use a date in the past!'))
# 			
# 			#check if date is in the right range
# 			if data > datetime.date.today() + datetime.timedelta(weeks=4):
# 				raise ValidationError(_('Date must be between today and 4 weeks from today'))
# 
# 			# return the cleaned data
# 			return data
