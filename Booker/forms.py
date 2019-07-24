from django.forms import ModelForm, Form
from django import forms
from .models import Activities
from UserConfs.models import UserCategories, SheetBases
import datetime
import monthdelta

def getDateSet():
    dt_now = datetime.datetime.now().date().replace(day=1)
    cur_date = dt_now.strftime("%Y-%m-01")
    date_choicelist = []

    for i in reversed(range(-3, 3)):
        dt = dt_now - monthdelta.monthdelta(i)
        key = dt.strftime("%Y-%m-01")
        value = dt.strftime("%B %Y")
        date_choicelist.append([key, value])

    return cur_date, date_choicelist

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

def basesheet_select2(field_id, user):
    choices = [(s.id, s.name) for s in SheetBases.objects.filter(user=user)]
    return generic_select2(field_id, choices)

class AddSheetForm(Form):
    cur_date, date_choicelist = getDateSet()
    add_sheet_date = generic_select2('add_sheet_period', date_choicelist, initial=cur_date)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['add_sheetbase_id'] =  basesheet_select2('add_sheetbase_id', user)

class FiltersForm(Form):
    cur_date, date_choicelist = getDateSet()
    filter_sheetbase_name = generic_char_input('filter_sheetbase_name', placeholder='sheet name contains')
    filter_date_from = generic_select2('filterFormDateFrom', date_choicelist, initial=date_choicelist[1])
    filter_date_to = generic_select2('filterFormDateTo', date_choicelist, initial=date_choicelist[-1])






