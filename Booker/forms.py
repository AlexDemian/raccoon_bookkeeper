from django.forms import ModelForm, Form
from django import forms
from .models import Activities
from UserConfs.models import UserCategories
import datetime
import calendar

def getDateSet():
    months_range = calendar.month_name
    dt_now = datetime.datetime.now()
    cur_month = dt_now.month
    cur_year = dt_now.year
    cur_date = '%s-%s-01' % (cur_year, str(cur_month).zfill(2))

    date_choicelist = []

    for i in range(-3, 3):
        year = cur_year
        month_index = cur_month + i

        if month_index == 0:
            year -= 1
            month_index = 12 - month_index

        key = '%s-%s-01' % (year, str(month_index).zfill(2))
        value = '%s %s' % (year, months_range[month_index])
        date_choicelist.append([key, value])
    return cur_date,  date_choicelist

def generic_select2(field_id, choices, multiple=False, **kwargs):

    return forms.ChoiceField(
            widget=forms.Select(
                attrs={
                    'id': field_id,
                    'class': 'select2_bootstrap',
                    'multiple': multiple,
                    'style': 'width: 100%',

                    },

            ),
            initial=kwargs.get('initial'),
            choices=choices,
            required=True)

def generic_char_input(field_id, max_length=30, placeholder=''):
    return forms.CharField(
        max_length=max_length,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'id': field_id,
                'placeholder': placeholder
            }),
        required=True)

def generic_float_input(field_id, placeholder='10.4'):
    return forms.FloatField(
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'id': field_id,
                'placeholder': placeholder
            }),
        required=True)

def period_select2(field_id):
    cur_date, date_choicelist = getDateSet()
    return generic_select2(field_id, date_choicelist, initial=cur_date)


class AddSheetForm(Form):
    add_sheet_name = generic_char_input('add_sheet_name', max_length=50, placeholder='sheet name')
    add_sheet_date = period_select2('add_sheet_period')

class FiltersForm(Form):
    cur_date, date_choicelist = getDateSet()
    filter_name = generic_char_input('filterFormSheetName', placeholder='name includes')
    filter_date_from = generic_select2('filterFormDateFrom', date_choicelist, initial=cur_date)
    filter_date_to = generic_select2('filterFormDateTo', date_choicelist, initial=cur_date)

class AddActivityForm(ModelForm):

    def __init__(self, *args, **kwargs):
        uid = kwargs.pop('uid', None)
        super(AddActivityForm, self).__init__(*args, **kwargs)

        if uid:
            print 'uid', uid
            self.fields['category'].widget.choices = [[cat.name, cat.name] for cat in UserCategories.objects.filter(user=uid)]

    class Meta:
        model = Activities
        fields = ['name', 'category', 'descr', 'value']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(
                attrs={
                    'class': 'select2_bootstrap',
                    'style': 'width: 100%;'
                },

            ),
            'descr': forms.TextInput(attrs={'class': 'form-control'}),
            'value': forms.TextInput(attrs={'class': 'form-control'}),
        }


