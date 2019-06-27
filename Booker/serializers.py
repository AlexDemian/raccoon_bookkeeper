from rest_framework import serializers
from .models import Activities

class ActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        fields = ('name', 'user', 'sheet', 'descr', 'category', 'value', 'pinned', 'active')

