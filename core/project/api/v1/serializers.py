from rest_framework import serializers
from project.models import Apps
from core.settings import BASE_URL

class ManageAppsSerializer(serializers.ModelSerializer):
    """
    Managing all the apps fields in CRUD operations.
    """
    run_container = serializers.SerializerMethodField()
    class Meta:
        model = Apps
        fields = "__all__"

    # providing a url for each app for easy access to run it's container
    def get_run_container(self, obj):
        return f"http://{BASE_URL}/run_container/{obj.id}/"


class ContainerMonitoringSerializer(serializers.Serializer):
    """
    Monitoring all of the containers (exited or running)
    """
    id = serializers.SerializerMethodField()
    name = serializers.CharField(max_length=255)
    status = serializers.SerializerMethodField()
    args = serializers.SerializerMethodField()
    started_at = serializers.SerializerMethodField()
    finished_at = serializers.SerializerMethodField()

    def get_status(self, obj):
        return obj.attrs['State']['Status']

    def get_id(self, obj):
        return obj.attrs['Id']
    
    def get_args(self, obj):
        return obj.attrs['Args']

    def get_started_at(self, obj):
        return obj.attrs['State']['StartedAt']

    def get_finished_at(self, obj):
        finished_at_time = obj.attrs['State'].get('FinishedAt')
        if finished_at_time == "0001-01-01T00:00:00Z":
            return "None"
        return finished_at_time


class RunContainerSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj.attrs['Id']

    def get_image(self, obj):
        return obj.attrs['Image']