from django import forms
from booker.models import Activities, UserCategories
import datetime
import calendar

def getDateSet():
    months_range = calendar.month_name[1:-1]
    dt_now = datetime.datetime.now()
    cur_month, cur_year = int(dt_now.strftime('%m')), int(dt_now.strftime('%Y'))
    cur_date = '%s-%s' % (cur_year, str(cur_month).zfill(2))

    date_choicedict = {}

    for year in range(cur_year - 1, cur_year + 2):
        for index, name in zip( range(1, len(months_range)+1), months_range ):
            date_choicedict['%s-%s' % (year, str(index).zfill(2))] = '%s %s' % (name, year)

    date_choicelist = [[key, date_choicedict[key]] for key in sorted(date_choicedict.keys())]
    return cur_date, date_choicedict, date_choicelist

class AddCostForm(forms.Form):

    def __init__(self, *args, **kwargs):
        cur_date, date_choicedict, date_choicelist = getDateSet()

        DateSelected = kwargs.pop('DateSelected')

        if not DateSelected:
            selected_date = (cur_date, date_choicedict[cur_date][1])

        else:
            selected_date = (DateSelected, date_choicedict[DateSelected][1])

        user_categories = [cat[0] for cat in UserCategories.objects.filter(user_id=kwargs.pop('user_id'), active=True).values_list('name')]
        super(AddCostForm, self).__init__(*args, **kwargs)
        self.fields['addFormCategory'] = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), choices=[[cat, cat] for cat in user_categories])
        self.fields['addFormDateSelectList'] = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-control"}), choices=date_choicelist, initial=selected_date, required=True)

    addFormDescr = forms.CharField(max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}), required=True)
    addFormPrice = forms.FloatField(widget=forms.TextInput(attrs={"class": "form-control"}), required=True)


class FiltersForm(forms.Form):

    def __init__(self, *args, **kwargs):
        cur_date, date_choicedict, date_choicelist = getDateSet()

        user_categories = [cat[0] for cat in UserCategories.objects.filter(user_id=kwargs.pop('user_id')).values_list('name')]

        DateFromSelected = kwargs.pop('DateFromSelected')
        DateToSelected = kwargs.pop('DateToSelected')

        selected_date_from = (DateFromSelected, date_choicedict[DateFromSelected][1]) if DateFromSelected else (cur_date, date_choicedict[cur_date][1])
        selected_date_to = (DateToSelected, date_choicedict[DateToSelected][1]) if DateToSelected else (cur_date, date_choicedict[cur_date][1])

        super(FiltersForm, self).__init__(*args, **kwargs)
        self.fields['filterFormCategory'] = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), choices=[[cat, cat] for cat in user_categories])
        self.fields['filterFormDateFromSelectList'] = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), choices=date_choicelist, initial=selected_date_from)
        self.fields['filterFormDateToSelectList'] = forms.ChoiceField(widget=forms.Select(attrs={"class": "form-control"}), choices=date_choicelist, initial=selected_date_to)

