from rest_framework.serializers import ModelSerializer
from project.models import Apps

class ManageAppsSerializer(ModelSerializer):
    class Meta:
        model = Apps
        fields = "__all__"