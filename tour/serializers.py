from rest_framework import serializers
from tour.models import Tour, Step


class TourSerializer(serializers.ModelSerializer):
    steps = serializers.SerializerMethodField('get_first_step')

    class Meta:
        model = Tour
        fields = ('name', 'display_name', 'complete_url', 'steps')

    def get_first_step(self, tour):
        return [
            StepSerializer(child_step, context=self.context).data
            for child_step in tour.load_tour_class().get_steps(0)
        ]


class StepSerializer(serializers.ModelSerializer):
    steps = serializers.SerializerMethodField('get_first_step')
    complete = serializers.SerializerMethodField('get_complete_for_user')

    class Meta:
        model = Step
        fields = ('name', 'display_name', 'url', 'sort_order', 'steps', 'complete')

    def get_first_step(self, step):
        return [
            StepSerializer(child_step, context=self.context).data
            for child_step in step.load_step_class().get_steps(0)
        ]

    def get_complete_for_user(self, step):
        if 'request' in self.context:
            return step.load_step_class().is_complete(self.context['request'].user)
        return False
