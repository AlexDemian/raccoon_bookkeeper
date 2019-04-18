# -*- coding: utf-8 -*-
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


class SettingsView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'user_confs/index.html')
