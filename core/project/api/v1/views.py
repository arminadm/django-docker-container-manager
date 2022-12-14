import docker
from rest_framework.views import Response
from rest_framework.viewsets import ViewSet
from rest_framework.mixins import UpdateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework import status
from django.shortcuts import get_object_or_404
from project.models import Apps
from .serializers import (
    ManageAppsSerializer,
    ContainerMonitoringSerializer,
    RunContainerSerializer
)

class ManageAppsViews(ViewSet, UpdateModelMixin):
    """
    CRUD operations for managing all the apps
    """
    serializer_class = ManageAppsSerializer
    queryset = Apps.objects.all()

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, pk=None):
        app = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(app)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None, *args, **kwargs):
        app = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(app, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk):
        app = get_object_or_404(self.queryset, pk=pk)
        app.delete()
        return Response({'detail':f'app object {pk} removed successfully'}, status=status.HTTP_204_NO_CONTENT)


class RunContainerView(GenericAPIView):
    """
    Run a container from an app
    """
    serializer_class = RunContainerSerializer

    def get(self, request, pk=None):
        app = get_object_or_404(Apps, pk=pk)
        client = docker.from_env()
        try:
            container = client.containers.run(
                name=app.name.replace(" ", "_"),
                image=app.image,
                environment=app.envs,
                command=app.command,
                detach=True,
            )
        except Exception as e:
            # error handling: conflict with existing container name
            if e.response.status_code == 409:
                copy_counter = 1
                resolve_name_conflict = True
                # keep trying to run this container until we reach unique name
                while(resolve_name_conflict):
                    try:
                        container = client.containers.run(
                            name=app.name.replace(" ", "_")+f"_copy_{copy_counter}",
                            image=app.image,
                            environment=app.envs,
                            command=app.command,
                            detach=True,
                        )
                        resolve_name_conflict = False
                    except Exception as e:
                        if e.response.status_code == 409:
                            # this copy has already chosen
                            # raise counter and try again
                            resolve_name_conflict = True
                            copy_counter += 1
                        else:
                            return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)    
            
            # error handling: others
            else:
                return Response({"error": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)   

        serializer = self.serializer_class(container)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ContainerMonitoringView(GenericAPIView):
    serializer_class = ContainerMonitoringSerializer
    def get_queryset(self):
        client = docker.from_env()
        return client.containers.list(all=True)

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data)