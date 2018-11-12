# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#Http tools
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
# Models
from django.contrib.auth.models import User
from booker.models import Activities, UserCategories
from django.db.models import Sum
# Forms
from .forms import AddCostForm, FiltersForm
from django import forms
# Auth tools
from django.contrib import auth

from django.views import View
# Other
import json





def get_period_filter(request):
    if 'filterFormDateFromSelectList' in request.POST and 'filterFormDateToSelectList' in request.POST:
        date_from = '%s-01' % request.POST['filterFormDateFromSelectList']
        date_to = '%s-01' % request.POST['filterFormDateToSelectList']

    else:
        date_from, date_to = '2018-03-01', '2018-09-01'

    return (date_from, date_to)




class Index(View):
    template_name = 'index.html'

    context = {

        'tables_columns': [
            ['Toggle', 5],
            ['Pin it!', 5],
            ['Description', 40],
            ['Category', 35],
            ['Price', 10],
            ['Delete', 5]
        ],
    }

    def dispatch(self, request, *args, **kwargs):
        user = auth.get_user(request)
        self.context['tables'] = []
        self.context['alerts'] = []
        self.context['username'], self.user_id = user.username, user.id
        self.get_all()
        self.context['add_form'] = AddCostForm(request.POST or None, user_id=self.user_id, DateSelected=None)
        self.context['filter_form'] = FiltersForm(request.POST or None, user_id=self.user_id, DateFromSelected=None, DateToSelected=None)
        return super(Index, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, self.context)

    def post(self, request):
        self.context['add_form'].DateSelected = self.request.POST['addFormDateSelectList']
        self.context['filter_form'].DateFromSelected = self.request.POST['filterFormDateFromSelectList']
        self.context['filter_form'].DateToSelected = self.request.POST['filterFormDateToSelectList']

        method_name = 'row_%s' % self.request.POST['action_type']
        if hasattr(self, method_name):
            getattr(self, method_name)()

        else:
            self.context['alerts'].append("What are you doing, little hacker?")

        return render(request, self.template_name, self.context)

    def get_all(self):

        user_categories = UserCategories.objects.filter(user_id=self.user_id)
        user_costs_categories = user_categories.filter(type='-').values('name')
        user_earnings_categories = user_categories.filter(type='+').values('name')

        query_set = Activities.objects.filter(user_id=self.user_id, date__range=get_period_filter(self.request))
        all_periods = query_set.values_list('date').distinct('date').order_by('-date')

        for period in all_periods:
            period_data = query_set.filter(date=period[0])

            period_earnings = period_data.filter(category__in=user_earnings_categories)
            period_costs = period_data.filter(category__in=user_costs_categories)

            categories_costs = period_costs.filter(category__in=user_costs_categories).values('category').annotate(Sum('price'))

            table = {
                'period': period[0].strftime("%B %Y"),
                'person_earnings':  period_earnings.values('id', 'descr', 'price').order_by('-pinned', 'category'),
                'total_earnings': period_earnings.aggregate(Sum('price'))['price__sum'],
                'person_costs': period_costs.filter(category__in=user_costs_categories).values('id', 'descr', 'category', 'price', 'toggle', 'pinned').order_by('-pinned', 'category'),
                'total_costs': period_costs.aggregate(Sum('price'))['price__sum'],
                'chart_data': json.dumps([{'y': row['price__sum'], 'name': row['category']} for row in categories_costs])
            }

            table["delta"] = (table['total_earnings'] or 0) - (table['total_costs'] or 0)
            self.context["tables"].append(table)

    def row_add(self):

        if self.context['add_form'].is_valid():

            Activities(
                user_id=self.request.user.id,
                date='%s-01' % self.request.POST['addFormDateSelectList'],
                descr=self.request.POST['addFormDescr'],
                category=self.request.POST['addFormCategory'],
                price=self.request.POST['addFormPrice'],
            ).save()

        else:
            self.context['alerts'].append('Input error!')

    def row_delete(self):
        Activities.objects.filter(id=self.request.POST['rowId'], user_id=self.user_id).delete()

    def row_pin(self):
        query_set = Activities.objects.get(id=self.request.POST['rowId'], user_id=self.user_id)
        query_set.pinned = not query_set.pinned
        query_set.save()


    def row_toggle(self):
        query_set = Activities.objects.get(id=self.request.POST['rowId'], user_id=self.user_id)
        query_set.toggle = not query_set.toggle
        query_set.save()

    def row_filter(self):
        pass


