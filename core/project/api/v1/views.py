from rest_framework.views import Response
from rest_framework.viewsets import ViewSet
from django.shortcuts import get_object_or_404
from project.models import Apps
from .serializers import ManageAppsSerializer

class ManageAppsViews(ViewSet):
    """
    CRUD operations for managing all the apps
    """
    serializer_class = ManageAppsSerializer
    queryset = Apps.objects.all()

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def retrieve(self, request, pk):
        app = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(app)
        return Response(serializer.data)
    
    def update(self, request, pk):
        app = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(app, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk):
        app = get_object_or_404(self.queryset, pk=pk)
        app.delete()
        return Response({'detail':f'app object {pk} removed successfully'})