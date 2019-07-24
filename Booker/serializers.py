from rest_framework import serializers
from .models import Activities


class ActivitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activities
        fields = ('__all__')

    def to_representation(self, instance):
        positive_category = instance.category.positive
        r = super().to_representation(instance)
        r['positive_category'] = positive_category
        return dict(r)

    def to_internal_value(self, instance):
        instance['origin_value'] = instance.get('origin_value') or instance['value']
        instance['name'] = instance.get('name') or 'nameless'
        return super().to_internal_value(instance)