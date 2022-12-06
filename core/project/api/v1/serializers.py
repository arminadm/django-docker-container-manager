from rest_framework import serializers
from project.models import Apps

class ManageAppsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apps
        fields = "__all__"

    #TODO: ADD run container link to each app