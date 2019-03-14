# -*- coding: utf-8 -*-
from __future__ import unicode_literals

#Http tools
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
# Models
from django.contrib.auth.models import User
from .models import Activities, Sheets
from UserConfs.models import UserCategories
from django.db.models import Sum, Q
# Forms
from .forms import AddSheetForm, FiltersForm, AddActivityForm
from django import forms
# Auth tools
from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
# Other
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string
import json
import calendar

class Index(LoginRequiredMixin, View):
    template_name = 'booker/index_base.html'
    def get(self, request):
        context = {
            'add_sheet_form': AddSheetForm(),
            'filter_form': FiltersForm(),
            'user': request.user
        }
        return render(request, self.template_name, context)


class SheetsView(LoginRequiredMixin, View):

    def get(self, request):
        if not request.GET.get('target'):
            return redirect("index")

        action = 'get_%s' % request.GET.get('target')
        if hasattr(SheetsView, action):
            return getattr(SheetsView(), action)(request)

        else:
            return JsonResponse({'status': False, 'message': 'Unexpected action: %s' % action})

    def post(self, request):
        if not request.POST.get('action'):
            return redirect("index")

        action = 'post_%s' % request.POST.get('action')
        if hasattr(SheetsView, action):
            return getattr(SheetsView(), action)(request)

        else:
            return JsonResponse({'status': False, 'message': 'Unexpected action: %s' % action})

    def get_sheets_ids(self, request):
        filters = Q(user=request.user)

        if request.GET.get('filter_date_from') and request.GET.get('filter_date_to'):
            filters &= Q(date__range=[request.GET.get('filter_date_from'), request.GET.get('filter_date_to')])

        if request.GET.get('filter_name'):
            filters &= Q(name__icontains=request.GET.get('filter_name'))

        sheets = [s[0] for s in Sheets.objects.filter(filters).values_list('id')]
        return render(request, 'booker/sheets_loader.html', {'sheets': sheets})

    def get_sheets(self, request):
        response = []
        add_activity_form = AddActivityForm(uid=request.user)
        ids = request.GET.getlist('sheet_ids[]', [])

        if ids:
            sheets = Sheets.objects.filter(id__in=ids, user_id=request.user)

            for sheet in sheets:
                all_activities = Activities.objects.filter(sheet=sheet)
                costs = all_activities.filter(value__lt=0)
                costs_sum = sum([c.value for c in costs])
                earnings_sum = sum([c.value for c in all_activities.filter(value__gt=0)])
                graph_data = [{'y': act["sum"], 'name': act["category"]} for act in costs.values('category').annotate(sum=Sum('value'))]

                context = {
                    'period': '%s %s' % (calendar.month_name[sheet.date.month], sheet.date.year),
                    'activities': all_activities,
                    'sheet': sheet,
                    'add_activity_form': add_activity_form,
                    'chart_data': json.dumps(graph_data),
                    'costs_sum': costs_sum,
                    'earnings_sum': earnings_sum
                }
                response.append({
                    'html': render_to_string('booker/sheet.html', context, request=request),
                    'id': sheet.id
                })

        return JsonResponse({'status': True, 'sheets': response})

    # Make it via modelform!
    # And check form is valid
    def post_add(self, request):
        Sheets(name=request.POST.get('add_sheet_name'), date=request.POST.get('add_sheet_date'), user=request.user).save()
        return JsonResponse({'status': True})


    def post_delete(self, request):
        pass


class ActivitiesView(LoginRequiredMixin, View):

    def post(self, request):
        action = 'post_%s' % request.POST.get('action')
        if hasattr(ActivitiesView, action):
            return getattr(ActivitiesView(), action)(request)

        else:
            return JsonResponse({'status': False, 'message': 'Unexpected action'})


    def post_add(self, request):
        try:
            sheet = Sheets.objects.get(id=request.POST.get("sheet"), user=request.user)

        except ObjectDoesNotExist:
            return JsonResponse({'status': False, 'message': 'Sheet does not exist'})


        form = AddActivityForm(request.POST)

        if form.is_valid():

            kwargs = {
                'name': form.cleaned_data['name'],
                'descr': form.cleaned_data['descr'],
                'category': form.cleaned_data['category'],
                'value': form.cleaned_data['value']
            }
            Activities(user=request.user, sheet=sheet, **kwargs).save()

            return JsonResponse({'status': True})

        else:
            return JsonResponse({'status': False, 'message': str(form.errors)}) 

    def post_edit(self):
        pass

    def post_delete(self, request):
        Activities.objects.filter(user=request.user, id=request.POST.get('id')).delete()
        return JsonResponse({'status': True})


class CategoriesView(LoginRequiredMixin, View):

    def post(self, request):
        action = 'post_%s' % request.POST.get('action')
        if hasattr(CategoriesView, action):
            return getattr(CategoriesView(), action)(request)

        else:
            return JsonResponse({'status': False, 'message': 'Unexpected action'})

    def post_add(self, request):
        name = request.POST.get('name')
        type = request.POST.get('type')
        UserCategories(user=request.user, name=name, type=type).save()
        return JsonResponse({'status': True})



class Index_OLD(LoginRequiredMixin, View):

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


