from django.urls import path
from .views import ManageAppsViews

urlpatterns = [
    path("manage_apps/", ManageAppsViews.as_view(), name='manage-apps')
]
