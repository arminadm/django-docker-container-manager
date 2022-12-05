from django.urls import path
from .views import ManageAppsViews

urlpatterns = [
    path("manage_apps/", ManageAppsViews.as_view({"get":"list", "post":"create"}), name='manage-apps-list'),
    path("manage_apps/detail/<int:pk>/", ManageAppsViews.as_view({"get":"retrieve", "put":"update", "delete":"destroy"}), name='manage-apps-detail')
]
