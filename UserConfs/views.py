# -*- coding: utf-8 -*-
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from .models import SheetBases, UserCategories, categories_colors_palette
from django.core import serializers
import json

def get_request(request):
    return json.loads(request.body.decode('utf-8'))


class BsheetCreate(LoginRequiredMixin, View):
    def post(self, request):
        kwargs = get_request(request)
        sb = SheetBases(user=request.user, name=kwargs['name'])
        sb.save()
        return JsonResponse({'status': True, 'pk': sb.pk})

class BsheetUpdate(LoginRequiredMixin, View):
    def post(self, request):
        kwargs = get_request(request)
        SheetBases.objects.filter(pk=kwargs.pop('pk'), user=request.user).update(**kwargs)
        return JsonResponse({'status': True})

class BsheetDelete(LoginRequiredMixin, View):
    def post(self, request):
        kwargs = get_request(request)
        SheetBases(pk=kwargs['pk'], user=request.user).delete()
        return JsonResponse({'status': True})

class CategoryCreate(LoginRequiredMixin, View):
    def post(self, request):
        kwargs = get_request(request)
        kwargs['sheetbase'] = SheetBases.objects.get(pk=kwargs['sheetbase'])
        kwargs['user'] = request.user
        cat = UserCategories(**kwargs)
        cat.save()
        return JsonResponse({'status': True, 'pk': cat.pk})

class CategoryUpdate(LoginRequiredMixin, View):
    def post(self, request):
        kwargs = get_request(request)
        pk = kwargs.pop('pk')
        UserCategories.objects.filter(pk=pk, user=request.user).update(**kwargs)
        return JsonResponse({'status': True})

class CategoryDelete(LoginRequiredMixin, View):
    def post(self, request):
        kwargs = get_request(request)
        UserCategories(pk=kwargs['pk'], user=request.user).delete()
        return JsonResponse({'status': True})

class SheetSettingsView(LoginRequiredMixin, View):
    def get(self, request):

        context = {
            'bsheets':  serializers.serialize('json', SheetBases.objects.filter(user=request.user).order_by('name')),
            'categories':  serializers.serialize('json', UserCategories.objects.filter(user=request.user).order_by('-positive', 'name')),
            'colors_palette': json.dumps(categories_colors_palette)
        }

        return render(request, 'user_confs/sheet_settings.html', context)

class AccountSettingsView(LoginRequiredMixin, View):
    def get(self, request):
        context = {}
        return render(request, 'user_confs/account_settings.html', context)
