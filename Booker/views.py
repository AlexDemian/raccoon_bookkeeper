# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

from .models import Activities, Sheets
from UserConfs.models import UserCategories, SheetBases
from django.db.models import Q

from .forms import AddSheetForm, FiltersForm
from django import forms

from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.views import View

from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string

from django.core import serializers
from django.forms.models import model_to_dict

from rest_framework import viewsets
from .serializers import ActivitiesSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

import json
import calendar
import datetime

class Index(LoginRequiredMixin, View):
    template_name = 'booker/index.html'
    def get(self, request):
        context = {
            'add_sheet_form': AddSheetForm(user=request.user),
            'filter_sheet_form': FiltersForm(),
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
        filters = Q(user=request.user, deleted=False)

        if request.GET.get('filter_date_from') and request.GET.get('filter_date_to'):
            filters &= Q(date__range=[request.GET.get('filter_date_from'), request.GET.get('filter_date_to')])

        if request.GET.get('filter_sheetbase_name'):
            filters &= Q(name__icontains=request.GET.get('filter_sheetbase_name'))

        sheets = [s[0] for s in Sheets.objects.filter(filters).values_list('id').order_by('date')]

        return render(request, 'booker/sheets_loader.html', {'sheets': sheets})

    def get_sheets(self, request):
        response = []

        ids = request.GET.getlist('sheet_ids[]', [])

        if ids:
            sheets = Sheets.objects.filter(id__in=ids, user_id=request.user, deleted=False)

            for sheet in sheets:

                context = {
                    'period': '%s %s' % (calendar.month_name[sheet.date.month], sheet.date.year),
                    'activities': serializers.serialize("json", Activities.objects.filter(sheet=sheet)),
                    'sheet': sheet,
                    'categories': serializers.serialize("json", UserCategories.objects.filter(sheetbase=sheet.sheetbase, user=request.user))
                }
                response.append({
                    'html': render_to_string('booker/sheet.html', context, request=request),
                    'id': sheet.id
                })

        return JsonResponse({'status': True, 'sheets': response})




class SheetCreate(LoginRequiredMixin, View):

    def post(self, request):
        sheetbase = SheetBases.objects.filter(pk=request.POST.get('add_sheetbase_id'), user=request.user)[0]
        Sheets(date=datetime.datetime.strptime(request.POST.get('add_sheet_date'), '%Y-%m-%d'), user=request.user, sheetbase=sheetbase).save()
        return JsonResponse({'status': True})


class SheetDelete(LoginRequiredMixin, View):

    def post(self, request):
        kwargs = json.loads(request.body.decode('utf-8'))
        try:
            Sheets.objects.filter(user=request.user, id=kwargs['sheet_id']).update(deleted=True)
            return JsonResponse({'status': True})

        except ObjectDoesNotExist:
            return JsonResponse({'status': False, 'message': 'Sheet does not exist'})

class SheetUpdate(LoginRequiredMixin, View):

    def post(self, request):
        kwargs = json.loads(request.body.decode('utf-8'))
        print(kwargs)
        try:
            Sheets.objects.filter(user=request.user, id=kwargs.pop('id', -1)).update(**kwargs)
            return JsonResponse({'status': True})

        except ObjectDoesNotExist:
            return JsonResponse({'status': False, 'message': 'Sheet does not exist'})


class ActivitiesViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = ActivitiesSerializer
    queryset = Activities.objects.all()


    def perform_create(self, serializer):
        kwargs = {
            'user': self.request.user,
        }
        serializer.save(**kwargs)



class ActivityDelete(LoginRequiredMixin, View):
    def post(self, request):
        kwargs = json.loads(request.body.decode('utf-8'))
        Activities.objects.filter(user=request.user, id=kwargs['id']).update(deleted=Q(deleted=False))
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






