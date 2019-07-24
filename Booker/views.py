# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect

from .models import Activities, Sheets
from UserConfs.models import UserCategories, SheetBases
from django.db.models import Q, F

from .forms import AddSheetForm, FiltersForm
from django import forms

from django.contrib import auth
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

from django.views import View

from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import render_to_string

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.core import serializers
from .serializers import ActivitiesSerializer



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


class ActivitiesApi(APIView):
    serializer_class = ActivitiesSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(status=status.HTTP_200_OK)

    def put(self, request):
        kwargs = request.data
        kwargs['user'] = request.user.pk
        serializer = self.serializer_class(data=kwargs)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'validationErrors': serializer.errors}, status=status.HTTP_200_OK)

    def post(self, request):
        kwargs = request.data
        kwargs['user'] = request.user.pk

        activity = Activities.objects.get(pk=kwargs['id'])
        serializer = self.serializer_class(data=kwargs)

        if serializer.is_valid():
            serializer.update(activity, serializer.validated_data)
            return Response(status=status.HTTP_200_OK)
        else:

            return Response({'validationErrors': serializer.errors}, status=status.HTTP_200_OK)

    def delete(self, request):
        kwargs = request.data
        Activities.objects.filter(user=request.user, id=kwargs['id']).update(deleted=Q(deleted=False))
        return Response(status=status.HTTP_200_OK)


class SheetsApi(APIView):
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    def render(self, request, sheet):
        activities_qs = Activities.objects.filter(sheet=sheet)

        context = {
            'activities': json.dumps(ActivitiesSerializer(activities_qs, many=True).data),
            'sheet': sheet,
            'categories': json.dumps(
                list(UserCategories.objects.filter(sheetbase=sheet.sheetbase, user=request.user).values()))
        }

        return {
            'html': render_to_string('booker/sheet.html', context, request=request),
            'id': sheet.id
        }

    def get(self, request):
        kwargs = request.query_params
        response = []
        filters = Q(user=request.user, deleted=False)
        if kwargs.get('filter_date_from') and kwargs.get('filter_date_to'):
            filters &= Q(date__range=[kwargs.get('filter_date_from'), kwargs.get('filter_date_to')])

        if request.GET.get('filter_sheetbase_name'):
            filters &= Q(name__icontains=kwargs.get('filter_sheetbase_name'))

        sheets = Sheets.objects.filter(filters).order_by('date', 'sheetbase')

        for sheet in sheets:
            response.append(self.render(request, sheet))

        return Response({'sheets': response}, status=status.HTTP_200_OK)


    def post(self, request):
        kwargs = request.data
        try:
            Sheets.objects.filter(user=request.user, id=kwargs.pop('id', -1)).update(**kwargs)
            return Response(status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'validationError':  {'Sheet': ["sheet doesn't exists"]}}, status=status.HTTP_200_OK)


    def put(self, request):
        kwargs = request.data
        sheetbase = SheetBases.objects.filter(pk=kwargs['add_sheetbase_id'], user=request.user)[0]
        Sheets(date=datetime.datetime.strptime(kwargs['add_sheet_date'], '%Y-%m-%d'), user=request.user, sheetbase=sheetbase).save()
        return Response(status=status.HTTP_201_CREATED)

    def delete(self, request):
        kwargs = request.data

        try:
            Sheets.objects.filter(user=request.user, id=kwargs['sheet_id']).update(deleted=True)
            return Response(status=status.HTTP_200_OK)

        except ObjectDoesNotExist:
            return Response({'validationError':  {'Sheet': ["sheet doesn't exists"]}}, status=status.HTTP_200_OK)





