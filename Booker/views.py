# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

from .models import Activities, Sheets, SheetBases
from UserConfs.models import UserCategories
from django.db.models import Q

from .forms import AddSheetForm, FiltersForm, AddActivityForm
from django import forms

from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.views import View

from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string

from django.core import serializers

import json
import calendar

class Index(LoginRequiredMixin, View):
    template_name = 'booker/index.html'
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

        ids = request.GET.getlist('sheet_ids[]', [])

        if ids:
            sheets = Sheets.objects.filter(id__in=ids, user_id=request.user).order_by('-date')

            for sheet in sheets:
                all_activities = Activities.objects.filter(sheet=sheet)

                context = {
                    'period': '%s %s' % (calendar.month_name[sheet.date.month], sheet.date.year),
                    'activities': serializers.serialize("json", all_activities),
                    'sheet': sheet,
                    'categories': serializers.serialize("json", UserCategories.objects.filter(user=request.user, sheetbase=sheet.sheetbase))
                }
                response.append({
                    'html': render_to_string('booker/sheet.html', context, request=request),
                    'id': sheet.id
                })

        return JsonResponse({'status': True, 'sheets': response})

    # Make it via modelform!
    # And check form is valid


class SheetCreate(LoginRequiredMixin, View):

    def post(self, request):
        Sheets(date=request.POST.get('add_sheet_date'), user=request.user, sheetbase_id=request.POST.get('add_sheetbase_id')).save()
        return JsonResponse({'status': True})


class SheetDelete(LoginRequiredMixin, View):

    def post(self, request):
        kwargs = json.loads(request.body.decode('utf-8'))
        Sheets.objects.get(user=request.user, id=kwargs['sheet_id']).delete()
        return JsonResponse({'status': True})

    def post_delete(self, request):
        try:
            Sheets.objects.get(user=request.user, id=request.POST['sheet_id']).delete()
            return JsonResponse({'status': True})
            
        except ObjectDoesNotExist:
            return JsonResponse({'status': False, 'message': 'Sheet does not exist'})


class ActivityDelete(LoginRequiredMixin, View):
    def post(self, request):
        kwargs = json.loads(request.body.decode('utf-8'))
        Activities.objects.filter(user=request.user, id=kwargs['id']).delete()
        return JsonResponse({'status': True})


class ActivityAdd(LoginRequiredMixin, View):
    def post(self, request):
        kwargs = json.loads(request.body.decode('utf-8'))
        kwargs['sheet'] = Sheets(pk=kwargs['sheet'])
        kwargs['category'] = UserCategories(pk=kwargs['category'])
        act = Activities(**kwargs)
        act.user = request.user
        act.save()
        return JsonResponse({'pk': act.pk})


class ActivityUpdate(LoginRequiredMixin, View):
    def post(self, request):
        kwargs = json.loads(request.body.decode('utf-8'))
        act = Activities.objects.filter(pk=kwargs.pop('id'))
        act.update(**kwargs)
        return JsonResponse({'status': True})






